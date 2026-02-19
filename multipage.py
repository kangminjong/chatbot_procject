import streamlit as st

class MultiPage:
    def __init__(self) -> None:
        self.pages = []

    def add_page(self, title, func) -> None:
        self.pages.append({'title':title, 'function':func})

    def run(self):
        st.sidebar.title("⚾ MLB Statcast")
        st.sidebar.caption("AI Data Analysis")
        st.sidebar.markdown("---")
        page = st.sidebar.selectbox('메뉴', self.pages,
                                    format_func=lambda page:page['title'])
        page['function']()
