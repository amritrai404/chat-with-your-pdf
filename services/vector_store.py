"""FAISS vector store for similarity search."""

import numpy as np
import faiss


class VectorStore:
    """In-memory FAISS index with metadata sidecar."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata: list[dict] = []

    def add(self, embeddings: list[list[float]], metadata: list[dict]) -> None:
        """Add embeddings + their metadata to the index."""
        if len(embeddings) != len(metadata):
            raise ValueError("embeddings and metadata must have same length.")
        if not embeddings:
            return

        vectors = np.array(embeddings, dtype="float32")
        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dim {vectors.shape[1]} != index dim {self.dimension}."
            )

        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_embedding: list[float], top_k: int = 4) -> list[dict]:
        """
        Search for top_k nearest chunks.
        Returns list of {metadata..., score} sorted by distance (asc).
        """
        if self.index.ntotal == 0:
            return []

        query = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(query, min(top_k, self.index.ntotal))

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            item = dict(self.metadata[idx])
            item["score"] = float(dist)
            results.append(item)

        return results

    def reset(self) -> None:
        """Clear the index and metadata."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

    def size(self) -> int:
        return self.index.ntotal