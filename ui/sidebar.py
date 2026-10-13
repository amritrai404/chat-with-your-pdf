import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("📁 Document")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        return uploaded_file