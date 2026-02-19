import streamlit as st
from langchain_classic.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import prompts
from langchain_core.messages import HumanMessage, AIMessage
import json
@st.cache_resource
def get_chains(_llm, _db, _prompt):
    return create_sql_query_chain(_llm, _db, prompt=_prompt)

def get_chat_history():
        history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append(HumanMessage(content=m["content"]))
            else:
                history.append(AIMessage(content=m["content"]))
        return history


def app(db, llm):
    st.markdown("""
        <style>
            /* 1. 바깥쪽 모든 프레임과 빨간색/파란색 그림자 강제 제거 */
            div[data-testid="stChatInput"], 
            div[data-testid="stChatInput"] > div,
            div[data-testid="stChatInput"] > div > div {
                border: none !important;
                background-color: transparent !important;
                box-shadow: none !important;
                outline: none !important;
            }

            /* 2. 입력창 본체 스타일: 테두리 4px 고정 및 배경색 강제 */
            div[data-testid="stChatInput"] textarea {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                caret-color: #3b82f6 !important; /* 파란색 커서 */
                
                /* 높이를 100px로 어떤 상황에서도 고정 */
                height: 100px !important;
                min-height: 100px !important;
                max-height: 100px !important;
                
                font-size: 1.25rem !important;
                
                /* 테두리를 4px 회색으로 아주 두껍게 */
                border: 4px solid #D1D5DB !important; 
                border-radius: 15px !important;
                padding: 15px 50px 15px 15px !important;
                
                /* 애니메이션을 꺼서 떨림 현상 방지 */
                transition: none !important;
                box-shadow: none !important;
            }

            /* 3. 클릭(포커스) 시: 빨간색/파란색 잔상 없이 오직 테두리색만 변경 */
            div[data-testid="stChatInput"] textarea:focus {
                border: 4px solid #3b82f6 !important; /* 두꺼운 파란색 테두리로 변경 */
                box-shadow: none !important; /* 파란색 번짐 효과 제거 (눈 보호) */
                outline: none !important;
            }

            /* 4. 전송 버튼 위치 고정 및 크기 조절 */
            div[data-testid="stChatInput"] button {
                bottom: 15px !important;
                right: 15px !important;
                transform: scale(1.4) !important;
                color: #3b82f6 !important;
                background: none !important;
                border: none !important;
            }

            /* 5. 비활성화 상태(질문 직후)에도 크기/색상 유지 */
            div[data-testid="stChatInput"] textarea:disabled {
                height: 100px !important;
                border: 4px solid #D1D5DB !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("⚾ MLB Statcast Explorer")
    USER_AVATAR = "https://raw.githubusercontent.com/google/material-design-icons/master/png/social/person/materialicons/48dp/1x/baseline_person_black_48dp.png"
    BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/2570/2570534.png"
    
    user_input = st.chat_input("질문을 입력하세요")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message["content"])
            if "query" in message and message["query"]:
                with st.expander("실행된 SQL 쿼리 확인"):
                    st.code(message["query"], language="sql")
    sql_chain = get_chains(llm, db, prompts.sql_prompt)
    
    answer_chain = prompts.answer_prompt | llm | StrOutputParser()

    rephrase_chain = prompts.contextualize_prompt | llm | StrOutputParser()
    if user_input:
        
        
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_input)
        
        chat_history = get_chat_history()
        
        if len(chat_history) > 0:
            standalone_question = rephrase_chain.invoke({
                "chat_history": chat_history,
                "input": user_input
            })
        else:   
            standalone_question = user_input
        sql_query = sql_chain.invoke({
        "input": standalone_question,
        "question": standalone_question,
        "top_k": 1000
    })
        
        clean_sql = sql_query.replace("```sql", "").replace("```", "").strip()
        st.session_state.messages.append({"role": "user", "content": user_input, "query":clean_sql})
        with st.spinner("데이터베이스에서 정보를 찾고 있습니다..."):
            try:
                response_data = db.run(clean_sql)
                full_answer = answer_chain.invoke({
                    "question": user_input,
                    "data": response_data,
                    "query": clean_sql
                })
                with st.chat_message("assistant", avatar=BOT_AVATAR):
                    with st.expander("assistant"):
                        st.code(clean_sql, language="sql")
                    
                    if response_data:
                        st.write("데이터 조회 결과")
                        st.write(full_answer)
                    else:
                        st.write("조회된 결과가 없습니다")
                st.session_state.messages.append({"role": "assistant", "content": full_answer, "sql" : clean_sql})
                new_example = {"input" : user_input, "query" : clean_sql}
                with open("data/example.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(new_example, ensure_ascii=False) + "\n")
            except Exception as e:
                with st.chat_message("assistant", avatar=BOT_AVATAR):
                    st.warning("데이터를 조회하는 중에 문제가 발생했습니다.")
                    with st.expander("에러 디버깅 정보"):
                        st.write(e)