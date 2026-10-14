"""Chat with Your PDF — Streamlit entry point."""

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from ui.layout import render_header, render_document_info, render_footer
from ui.sidebar import render_upload_controls
from ui.chat import render_chat


st.set_page_config(
    page_title="Chat with Your PDF",
    page_icon="📄",
    layout="wide",
)

# ---------- Custom CSS: dark theme + clean look ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    section.main > div {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    .stFileUploader {
        background-color: #161A23;
        border-radius: 12px;
        padding: 8px;
    }
    .stChatMessage {
        background-color: #161A23;
        border-radius: 12px;
        padding: 6px 10px;
    }
    .source-box {
        background-color: #1B2130;
        border-left: 3px solid #FF4B4B;
        padding: 8px 12px;
        border-radius: 6px;
        margin-top: 6px;
        font-size: 0.85rem;
    }
    .footer {
        text-align: center;
        color: #8A93A6;
        font-size: 0.9rem;
        padding: 1.2rem 0 0.5rem 0;
        border-top: 1px solid #232A38;
        margin-top: 2rem;
    }
    .footer a {
        color: #FF4B4B;
        text-decoration: none;
        font-weight: 600;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        color: #8A93A6;
        font-size: 1rem;
        margin-bottom: 1.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

render_header()
render_upload_controls()
render_document_info()
st.divider()
render_chat()
render_footer()