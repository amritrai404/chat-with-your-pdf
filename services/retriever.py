"""High-level retrieval: query → relevant chunks."""

from services.embeddings import embed_query


def retrieve(
    query: str,
    vector_store,
    top_k: int = 4,
) -> list[dict]:
    """
    Retrieve top-k relevant chunks for a query.
    Returns list of chunks with metadata + score.
    """
    if not query or not query.strip():
        return []

    if vector_store.size() == 0:
        return []

    query_vec = embed_query(query)
    return vector_store.search(query_vec, top_k=top_k)