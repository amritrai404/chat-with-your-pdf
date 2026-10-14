"""Layout helpers: header, document info, footer."""

import streamlit as st


def render_header() -> None:
    st.markdown(
        '<div class="app-title">📄 Chat with Your PDF</div>'
        '<div class="app-subtitle">'
        'Upload a PDF, ask questions, get answers with page citations.'
        '</div>',
        unsafe_allow_html=True,
    )


def render_document_info() -> None:
    if not st.session_state.get("pdf_filename"):
        return

    st.markdown(
        f"**📄 Current Document:** `{st.session_state['pdf_filename']}`  \n"
        f"Pages: **{st.session_state.get('pdf_pages', '?')}** &nbsp;|&nbsp; "
        f"Chunks: **{st.session_state.get('pdf_chunks', '?')}**"
    )


def render_footer() -> None:
    st.markdown(
        '<div class="footer">'
        'Built by '
        '<a href="https://www.linkedin.com/in/amrit-rai-data-analyst/" target="_blank">'
        'Amrit Rai'
        '</a>'
        '</div>',
        unsafe_allow_html=True,
    )