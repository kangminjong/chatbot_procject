import streamlit as st

def app():
	st.write('''
	### 개발 환경을 구축한 차례에 따라 매뉴얼을 작성해 주세요. 
	conda create sesac_minjong_chatbot\n
	pip install streamlit\n
	pip install openai\n
	.streamlit 폴더생성\n
	pip install langchain\
	secrets.toml 설정파일 생성 (openaiapikey) 관리하기 위함\n
	pip install langchain langchain-community langchain-openai sqlalchemy psycopg2-binary(db 연동)
	''')
