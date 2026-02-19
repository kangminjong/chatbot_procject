from multipage import MultiPage
from page import project1 as p1
from page import project2 as p2
from page import intro
from page import chatbot
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

@st.cache_resource
def get_db():
    db_url = f"postgresql+psycopg2://{st.secrets['postgres']['username']}:{st.secrets['postgres']['password']}@{st.secrets['postgres']['host']}:{st.secrets['postgres']['port']}/{st.secrets['postgres']['database']}"
    return SQLDatabase.from_uri(db_url, schema="public", sample_rows_in_table_info=0, include_tables = ["mart_batter_total", "mart_batter_daily", "mart_pitcher_total", "mart_pitcher_daily", "mart_team_fielding", "mart_team_pitching", "mart_team_batting","dim_team_mapping"])

# 모델 생성
@st.cache_resource
def get_llm():
    return ChatOpenAI(model="gpt-4o", openai_api_key=st.secrets["OPENAI_API_KEY"])


db = get_db()
llm = get_llm()


page = MultiPage()

page.add_page("챗봇", lambda :chatbot.app(db,llm))
# page.add_page("인트로", intro.app) 
# page.add_page("매뉴얼", p1.app) 
# page.add_page("Data Flow Diagram", p2.app) 
page.run()