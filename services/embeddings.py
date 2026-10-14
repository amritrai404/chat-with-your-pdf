"""Local embeddings using sentence-transformers (free, no API)."""

import os
from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    """Load model once and cache."""
    model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    return SentenceTransformer(model_name)


def embed_texts(texts: list[str], model: str | None = None) -> list[list[float]]:
    """Embed list of texts locally. Returns list of vectors."""
    if not texts:
        return []

    cleaned = [t.strip() for t in texts]
    if any(not t for t in cleaned):
        raise ValueError("Cannot embed empty text.")

    st_model = _get_model()
    vectors = st_model.encode(
        cleaned,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return [v.tolist() for v in vectors]


def embed_query(query: str, model: str | None = None) -> list[float]:
    """Embed a single query string."""
    if not query or not query.strip():
        raise ValueError("Query is empty.")
    return embed_texts([query])[0]