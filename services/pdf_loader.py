"""PDF text extraction using PyMuPDF."""

import pymupdf  # modern import (fitz is deprecated)


def extract_pdf(file_bytes: bytes) -> dict:
    """
    Extract text from PDF bytes.
    Returns dict with:
      - pages: list of {page: int (1-indexed), text: str, has_text: bool}
      - total_pages: int
      - total_chars: int
      - is_scanned: bool (True if no text found on any page)
    """
    result = {
        "pages": [],
        "total_pages": 0,
        "total_chars": 0,
        "is_scanned": False,
    }

    try:
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Could not open PDF: {e}")

    result["total_pages"] = len(doc)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        text = text.strip()

        result["pages"].append({
            "page": page_num + 1,
            "text": text,
            "has_text": bool(text),
        })
        result["total_chars"] += len(text)

    doc.close()

    if result["total_chars"] == 0:
        result["is_scanned"] = True

    return result