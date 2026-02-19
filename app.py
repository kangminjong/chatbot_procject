import streamlit as st
from page import project1 as p1
from page import project2 as p2
from page import intro

st.title('Project')

item_list = ['item0','item1', 'item2']

item_labels = {'item0':'개발환경구축', 'item1':'스트림릿', 'item2':'Diagram'}

FIL = lambda x : item_labels[x]
item = st.sidebar.selectbox('항목을 골라요.',  item_list, format_func = FIL )

if item == 'item1':
	p1.app()
elif item == 'item2':
	p2.app()
elif item == 'item0':
	intro.app()
