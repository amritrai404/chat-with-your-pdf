"""File validation utilities."""

MAX_FILE_SIZE_MB = 20


def validate_uploaded_file(uploaded_file) -> tuple[bool, str]:
    """
    Validate uploaded file.
    Returns (is_valid, error_message).
    """
    if uploaded_file is None:
        return False, "No file uploaded."

    # Check extension
    if not uploaded_file.name.lower().endswith(".pdf"):
        return False, f"Invalid file type: '{uploaded_file.name}'. Only PDF files are allowed."

    # Check size
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large: {size_mb:.1f} MB. Max allowed: {MAX_FILE_SIZE_MB} MB."

    # Check empty file
    if uploaded_file.size == 0:
        return False, "File is empty."

    return True, ""