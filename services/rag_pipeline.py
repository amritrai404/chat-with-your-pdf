"""End-to-end RAG pipeline."""

import os
import streamlit as st

from services.pdf_loader import extract_pdf
from services.chunker import chunk_pages
from services.embeddings import embed_texts
from services.vector_store import VectorStore
from services.retriever import retrieve
from services.llm_service import generate_answer


def process_pdf(file_bytes: bytes, filename: str) -> dict:
    """
    Process a PDF: extract → chunk → embed → build index.
    Stores result in Streamlit session_state.
    """
    pdf_data = extract_pdf(file_bytes)

    if pdf_data["is_scanned"]:
        raise ValueError(
            "This PDF appears to be scanned (no extractable text). OCR is not supported yet."
        )

    chunk_size = int(os.getenv("CHUNK_SIZE", "700"))
    overlap = int(os.getenv("CHUNK_OVERLAP", "80"))
    chunks = chunk_pages(
        pdf_data["pages"], filename=filename,
        chunk_size=chunk_size, overlap=overlap,
    )

    if not chunks:
        raise ValueError("No text chunks could be created from this PDF.")

    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    dim = len(embeddings[0])
    store = VectorStore(dimension=dim)
    store.add(embeddings, chunks)

    st.session_state["vector_store"] = store
    st.session_state["pdf_filename"] = filename
    st.session_state["pdf_pages"] = pdf_data["total_pages"]
    st.session_state["pdf_chunks"] = len(chunks)

    return {
        "filename": filename,
        "pages": pdf_data["total_pages"],
        "chunks": len(chunks),
        "chars": pdf_data["total_chars"],
    }


def ask(question: str) -> dict:
    """Ask a question. Returns {answer, sources, fallback, model, key_used}."""
    store = st.session_state.get("vector_store")
    if store is None:
        return {
            "answer": "Please upload a PDF first.",
            "sources": [],
            "fallback": True,
            "model": "n/a",
            "key_used": "n/a",
        }

    top_k = int(os.getenv("TOP_K", "4"))
    chunks = retrieve(question, store, top_k=top_k)

    if not chunks:
        return {
            "answer": "I could not find this information in the provided document.",
            "sources": [],
            "fallback": True,
            "model": "n/a",
            "key_used": "n/a",
        }

    result = generate_answer(question, chunks)
    answer = result["answer"]
    model = result["model"]
    key_used = result.get("key_used", "n/a")

    # Increment request counter (only if LLM succeeded)
    if key_used != "none" and model != "n/a":
        st.session_state["requests_today"] = st.session_state.get("requests_today", 0) + 1

    fallback = "could not find" in answer.lower()

    sources = [
        {
            "filename": c["filename"],
            "page": c["page"],
            "score": c.get("score"),
            "text": c["text"][:300],
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "fallback": fallback,
        "model": model,
        "key_used": key_used,
    }


def reset_state() -> None:
    """Clear all PDF-related session state."""
    for key in ["vector_store", "pdf_filename", "pdf_pages", "pdf_chunks", "messages"]:
        st.session_state.pop(key, None)