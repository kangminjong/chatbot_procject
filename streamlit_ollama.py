from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


def run_ollama(message):
    llm = ChatOllama(model="gemma:latest")

    prompt = ChatPromptTemplate.from_template("{message}")

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"message": message})

    return answer


def main():
    st.title("My Local LLM")

    if 'history' not in st.session_state:
        st.session_state.history = []

    user_message = st.text_input("메시지를 입력하세요:")

    if st.button("입력"):
        if user_message:
            response = run_ollama(user_message)

            st.session_state.history.append(("User", user_message))
            st.session_state.history.append(("Bot", response))

            st.session_state.user_input = ""  # Optionally clear the input

    st.markdown("""
    <style>
    .user-message {
        background-color: #dcf8c6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: right;
    }
    .bot-message {
        background-color: #dcf8c6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        for speaker, message in st.session_state.history:
            if speaker == "User":
                st.markdown(f'<div class="user-message"><strong>{speaker}:</strong> {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message"><strong>{speaker}:</strong> {message}</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
