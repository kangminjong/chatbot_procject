import streamlit as st
from utils import project1_desc as p1d


def app():
	st.write('''
		### Streamlit 매뉴얼을 작성해 주세요. 
		'''
		)

	p1d.desc()
