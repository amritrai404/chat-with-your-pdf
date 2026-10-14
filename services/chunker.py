"""Split page texts into overlapping chunks with metadata."""


def chunk_pages(
    pages: list[dict],
    filename: str,
    chunk_size: int = 700,
    overlap: int = 80,
) -> list[dict]:
    """
    Split page texts into overlapping chunks.

    Args:
        pages: list of {page: int, text: str, has_text: bool}
        filename: source PDF filename
        chunk_size: approx characters per chunk
        overlap: characters of overlap between chunks

    Returns:
        list of chunks, each: {
            chunk_id, text, page, filename, char_start, char_end
        }
    """
    chunks = []
    chunk_id = 0

    for page_data in pages:
        if not page_data.get("has_text"):
            continue

        text = page_data["text"]
        page_num = page_data["page"]

        if len(text) <= chunk_size:
            chunks.append({
                "chunk_id": chunk_id,
                "text": text,
                "page": page_num,
                "filename": filename,
                "char_start": 0,
                "char_end": len(text),
            })
            chunk_id += 1
            continue

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "page": page_num,
                    "filename": filename,
                    "char_start": start,
                    "char_end": min(end, len(text)),
                })
                chunk_id += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks