# Chat with Your PDF

RAG-powered PDF Q&A app — upload a PDF, ask questions, get answers with exact page citations.

## Status
🚧 In development — Day 1: PDF upload + text extraction

## Tech Stack
- Streamlit (UI)
- PyMuPDF (PDF extraction)
- FAISS (vector search)
- OpenAI (embeddings + LLM)
- pytest (testing)

## Local Setup
```bash
git clone https://github.com/<username>/chat-with-your-pdf.git
cd chat-with-your-pdf
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env    # apni API key daalo
streamlit run app.py