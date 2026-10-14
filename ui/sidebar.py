"""Upload + reset controls (inline, no sidebar)."""

import streamlit as st

from utils.validators import validate_uploaded_file
from services.rag_pipeline import process_pdf, reset_state


def render_upload_controls() -> None:
    """Top-of-page upload + reset + counter row."""

    col_upload, col_reset, col_counter = st.columns([5, 1, 2])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload a PDF",
            type=["pdf"],
            key="pdf_uploader",
            label_visibility="collapsed",
        )

    with col_reset:
        if st.session_state.get("pdf_filename"):
            if st.button("🔄 Reset", use_container_width=True):
                # Save current session to history before reset
                if st.session_state.get("messages"):
                    snapshot = {
                        "pdf_filename": st.session_state["pdf_filename"],
                        "messages": st.session_state["messages"],
                        "vector_store": st.session_state.get("vector_store"),
                    }
                    history = st.session_state.get("chat_history", [])
                    history.append(snapshot)
                    st.session_state["chat_history"] = history[-3:]

                reset_state()
                st.rerun()
        else:
            st.write("")

    with col_counter:
        requests_used = st.session_state.get("requests_today", 0)
        st.metric("Requests (session)", f"{requests_used} / 100")

    if uploaded_file is not None:
        is_valid, error = validate_uploaded_file(uploaded_file)
        if not is_valid:
            st.error(error)
        else:
            if st.session_state.get("pdf_filename") != uploaded_file.name:
                with st.spinner("Processing PDF..."):
                    try:
                        summary = process_pdf(
                            uploaded_file.getvalue(),
                            uploaded_file.name,
                        )
                        st.success(
                            f"Loaded: {summary['filename']}  |  "
                            f"Pages: {summary['pages']}  |  "
                            f"Chunks: {summary['chunks']}"
                        )
                    except Exception as e:
                        st.error(f"Failed to process PDF: {e}")