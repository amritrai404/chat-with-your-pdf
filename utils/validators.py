def validate_pdf(uploaded_file) -> tuple[bool, str]:
    if uploaded_file is None:
        return False, "No file uploaded."
    if not uploaded_file.name.lower().endswith(".pdf"):
        return False, "Only PDF files allowed."
    return True, ""