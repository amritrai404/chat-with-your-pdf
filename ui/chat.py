"""Chat interface with persistent history (last 3 sessions)."""

import json
import streamlit as st
import streamlit.components.v1 as components

from services.rag_pipeline import ask
from utils.source_formatter import format_sources_markdown, format_evidence


# ---------- localStorage helpers via JS bridge ----------
def _save_history_to_browser(history: list) -> None:
    """Save last 3 chat sessions to browser localStorage."""
    data = json.dumps(history[-3:])  # keep only last 3 sessions
    js = f"""
    <script>
    try {{
        localStorage.setItem('chat_pdf_history', JSON.stringify({data}));
    }} catch (e) {{}}
    </script>
    """
    components.html(js, height=0, width=0)


def _load_history_from_browser() -> list:
    """Load last 3 chat sessions from browser localStorage."""
    js = """
    <script>
    (function() {
        try {
            const raw = localStorage.getItem('chat_pdf_history');
            if (raw) {
                window.parent.postMessage({
                    type: 'chat_pdf_history',
                    data: JSON.parse(raw)
                }, '*');
            }
        } catch (e) {}
    })();
    </script>
    """
    components.html(js, height=0, width=0)

    # Streamlit doesn't natively read JS→Python messages here,
    # so we rely on session_state loaded once.
    return st.session_state.get("history_loaded", [])


def _render_meta(msg: dict) -> None:
    """Show model + key used under an assistant message."""
    parts = []
    if msg.get("model") and msg["model"] != "n/a":
        parts.append(f"🧠 {msg['model']}")
    if msg.get("key_used") and msg["key_used"] != "n/a":
        parts.append(f"🔑 {msg['key_used']}")
    if parts:
        st.caption(" | ".join(parts))


def _render_message(msg: dict) -> None:
    """Render a single message from history."""
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            _render_meta(msg)
        if msg.get("sources_md"):
            st.markdown(
                f'<div class="source-box">{msg["sources_md"]}</div>',
                unsafe_allow_html=True,
            )
        if msg.get("evidence_md"):
            with st.expander("Show evidence"):
                st.markdown(msg["evidence_md"])


def render_chat() -> None:
    st.markdown("### 💬 Ask your PDF")

    # ---- Previous chat sessions (last 3) ----
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    history = st.session_state["chat_history"]

    if history:
        with st.expander(f"🕘 Previous chats ({len(history)})", expanded=False):
            for i, session in enumerate(reversed(history), 1):
                pdf_name = session.get("pdf_filename", "unknown.pdf")
                msg_count = len(session.get("messages", []))
                st.markdown(f"**{i}. {pdf_name}** — {msg_count} messages")
                if st.button(f"Load chat #{i}", key=f"load_{i}_{pdf_name}"):
                    st.session_state["messages"] = session["messages"]
                    st.session_state["pdf_filename"] = pdf_name
                    st.session_state["vector_store"] = session.get("vector_store")
                    st.rerun()

    # ---- Current chat ----
    if not st.session_state.get("pdf_filename"):
        st.info("👆 Upload a PDF above to get started.")
        return

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        _render_message(msg)

    question = st.chat_input("Ask a question about your PDF...")

    if question:
        st.session_state["messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask(question)

            st.markdown(result["answer"])

            meta = {
                "model": result.get("model", ""),
                "key_used": result.get("key_used", ""),
            }
            _render_meta(meta)

            sources_md = ""
            evidence_md = ""
            if result["sources"]:
                sources_md = format_sources_markdown(result["sources"])
                evidence_md = format_evidence(result["sources"])
                st.markdown(
                    f'<div class="source-box">{sources_md}</div>',
                    unsafe_allow_html=True,
                )
                with st.expander("Show evidence"):
                    st.markdown(evidence_md)

        st.session_state["messages"].append({
            "role": "assistant",
            "content": result["answer"],
            "model": result.get("model", ""),
            "key_used": result.get("key_used", ""),
            "sources_md": sources_md,
            "evidence_md": evidence_md,
        })

    # ---- Save current session snapshot to history ----
    if st.session_state["messages"] and st.session_state.get("pdf_filename"):
        snapshot = {
            "pdf_filename": st.session_state["pdf_filename"],
            "messages": st.session_state["messages"],
            "vector_store": st.session_state.get("vector_store"),
        }
        # Avoid duplicates — check if this session already exists
        history = st.session_state["chat_history"]
        if not history or history[-1].get("pdf_filename") != snapshot["pdf_filename"]:
            history.append(snapshot)
        else:
            history[-1] = snapshot  # update latest

        # Keep only last 3
        st.session_state["chat_history"] = history[-3:]