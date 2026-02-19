import streamlit as st
from utils import project2_desc as p2d


def app():
	st.write('''
		### 수행한 프로젝트의 Data Flow Diagram을 작성해 주세요. 
		'''
		)
	p2d.desc()
