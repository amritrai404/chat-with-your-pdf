import streamlit as st

def render_chat():
    st.subheader("💬 Chat")
    question = st.text_input("Ask a question about your PDF")
    if question:
        st.write(f"You asked: {question}")