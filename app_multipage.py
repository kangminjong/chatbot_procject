import streamlit as st
from multipage import MultiPage
from page import intro
from page import project1 as p1
from page import project2 as p2

app = MultiPage()

one_one_two = r'''$${\vdash}:.(\exists x,y).\alpha=\iota`x.\beta=\iota`y.\supset:\alpha\cup\beta\in2.\equiv.\alpha\cap\beta=\Lambda$$'''
st.write(one_one_two)

app.add_page('개발환경구축', intro.app)
app.add_page('스트림릿', p1.app)
app.add_page('Diagram',p2.app)

app.run()
