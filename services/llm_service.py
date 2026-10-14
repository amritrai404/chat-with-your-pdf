"""LLM answer generation via OpenRouter with API key fallback."""

import os
from openai import OpenAI


_clients: list[OpenAI] = []

SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly based on the provided PDF context.

Rules:
1. Answer ONLY using information from the provided context chunks.
2. If the context does not contain enough information, respond exactly with: "I could not find this information in the provided document."
3. Do NOT make up facts or use outside knowledge.
4. Keep answers concise and clear.
5. When helpful, mention which page the information comes from.
"""


def _get_clients() -> list[OpenAI]:
    """Build a list of OpenAI clients (one per API key). Cached."""
    global _clients
    if _clients:
        return _clients

    keys = []
    for var in ("OPENROUTER_API_KEY_1", "OPENROUTER_API_KEY_2", "OPENROUTER_API_KEY"):
        key = os.getenv(var)
        if key and key.strip():
            keys.append(key.strip())

    if not keys:
        raise ValueError(
            "No OpenRouter API key found. Set OPENROUTER_API_KEY_1 in .env"
        )

    _clients = [
        OpenAI(api_key=k, base_url="https://openrouter.ai/api/v1")
        for k in keys
    ]
    return _clients


def _build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a context block for the LLM."""
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(
            f"[Chunk {i} | File: {c['filename']} | Page: {c['page']}]\n{c['text']}"
        )
    return "\n\n".join(parts)


def generate_answer(question: str, chunks: list[dict]) -> dict:
    """
    Generate a grounded answer from retrieved chunks.
    Tries API key 1, falls back to key 2 if key 1 fails.
    Returns dict: {answer: str, model: str, key_used: str}
    """
    if not question or not question.strip():
        return {"answer": "Please ask a question.", "model": "n/a", "key_used": "n/a"}

    if not chunks:
        return {
            "answer": "I could not find this information in the provided document.",
            "model": "n/a",
            "key_used": "n/a",
        }

    model = os.getenv("LLM_MODEL", "openrouter/free")
    context = _build_context(chunks)

    user_message = (
        f"Context from the PDF:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer using only the context above."
    )

    clients = _get_clients()
    last_error = None

    for i, client in enumerate(clients, 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.2,
            )
            return {
                "answer": response.choices[0].message.content.strip(),
                "model": response.model,
                "key_used": f"key_{i}",
            }
        except Exception as e:
            last_error = e
            print(f"[llm_service] Key {i} failed: {type(e).__name__} — trying next...")
            continue

    return {
        "answer": f"All API keys failed. Last error: {type(last_error).__name__}: {last_error}",
        "model": "n/a",
        "key_used": "none",
    }