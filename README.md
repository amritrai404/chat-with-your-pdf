# 📄 Chat with Your PDF

> A RAG-powered (Retrieval-Augmented Generation) web app that lets you upload any PDF and ask questions in plain English — getting answers with **exact page citations**.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green.svg)](https://github.com/facebookresearch/faiss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---
## LIVE LINK: 
   https://chat-with-pdf-amritrai.streamlit.app/
---
## 🎯 Problem Statement

Large Language Models hallucinate. If you ask GPT "What is the attendance policy in my college handbook?", it will confidently make up a number.

**Chat with Your PDF** solves this by:

1. Extracting text from your PDF
2. Finding the most relevant sections using semantic search
3. Forcing the LLM to answer **only** from those sections
4. Showing you the **exact page** where the answer came from

If the answer isn't in the document, the app says so — no hallucinations.

---

## ✨ Features

- 📤 **Upload any PDF** (up to 20MB, text-based)
- 💬 **Natural language Q&A** — ask in plain English
- 🎯 **Page-level citations** — every answer shows the source page
- 🔍 **Evidence snippets** — see the exact text the answer came from
- 🛡️ **Grounded responses** — no hallucination, strict context-only prompting
- 🔄 **Dual API key fallback** — 2 OpenRouter keys, 100 requests/day
- 🌙 **Dark theme UI** — clean, modern, single-page layout
- 🚀 **Zero-cost embeddings** — runs locally via `sentence-transformers`
- 📊 **Session request counter** — track API usage
- 🔒 **Privacy-first** — PDFs never leave your machine (only chunks go to LLM)

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI (app.py)                    │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │  Upload PDF  │   │ Ask Question │   │ Show Answer  │    │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘    │
└─────────┼───────────────────┼───────────────────┼───────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ PDF Loader  │      │  Retriever  │      │ LLM Service │
│  (PyMuPDF)  │      │   (FAISS)   │      │ (OpenRouter)│
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Chunker   │      │  Embeddings │      │  Answer +   │
│             │      │   (local)   │      │   Sources   │
└─────────────┘      └─────────────┘      └─────────────┘
```

### RAG Pipeline Flow

```text
PDF Upload
    │
    ▼
 Extract text (PyMuPDF) → per-page text + metadata[1]
    │
    ▼
 Chunk (700 chars, 80 overlap) → chunks with {page, filename, chunk_id}[2]
    │
    ▼
 Embed chunks (all-MiniLM-L6-v2, local) → 384-dim vectors[3]
    │
    ▼
 Build FAISS index → in-memory L2 similarity[4]
    │
    ════════════════ User asks a question ════════════════
    │
    ▼
 Embed query (same local model)[5]
    │
    ▼
 FAISS search → top-4 relevant chunks[6]
    │
    ▼
 LLM call (OpenRouter, context-only prompt) → grounded answer[7]
    │
    ▼
 Format response → answer + filename + page + evidence[8]
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI** | Streamlit | Web interface |
| **PDF Parsing** | PyMuPDF (fitz) | Text extraction with page numbers |
| **Chunking** | Custom (character-based) | Overlapping chunks with metadata |
| **Embeddings** | sentence-transformers (`all-MiniLM-L6-v2`) | Local, free, 384-dim vectors |
| **Vector Search** | FAISS (`IndexFlatL2`) | Fast similarity search |
| **LLM** | OpenRouter (`openrouter/free` router) | Grounded answer generation |
| **Config** | python-dotenv | Environment variables |
| **Testing** | pytest | Unit tests |
| **Deployment** | Streamlit Community Cloud | Live hosting |

---

## 📁 Project Structure

```text
chat-with-pdf/
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git exclusions
├── README.md               # This file
├── .streamlit/
│   └── config.toml         # Streamlit dark theme config
├── ui/
│   ├── layout.py           # Header, document info, footer
│   ├── sidebar.py          # Upload + reset + counter controls
│   └── chat.py             # Chat interface
├── services/
│   ├── pdf_loader.py       # PyMuPDF text extraction
│   ├── chunker.py          # Overlapping chunking
│   ├── embeddings.py       # Local embeddings
│   ├── vector_store.py     # FAISS index wrapper
│   ├── retriever.py        # Query → top-k chunks
│   ├── llm_service.py      # OpenRouter LLM with key fallback
│   └── rag_pipeline.py     # End-to-end orchestration
├── utils/
│   ├── validators.py       # File validation
│   └── source_formatter.py # Citation formatting
├── tests/
│   └── test_*.py           # Unit tests
└── data/
    ├── sample_pdfs/        # Test PDFs
    └── indexes/            # (optional) saved FAISS indexes
```

---

## 🚀 Local Setup

### Prerequisites

- Python 3.10 or higher
- pip
- An OpenRouter API key (free): [openrouter.ai/keys](https://openrouter.ai/keys)

### Installation

```bash
# 1. Clone the repo
git clone [https://github.com/amritrai404/chat-with-your-pdf.git](https://github.com/amritrai404/chat-with-your-pdf.git)
cd chat-with-your-pdf

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OpenRouter API key(s)

# 5. Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`.

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY_1` | ✅ Yes | Primary OpenRouter API key |
| `OPENROUTER_API_KEY_2` | ⚠️ Optional | Fallback key (recommended) |
| `LLM_MODEL` | ✅ Yes | `openrouter/free` (auto-selects free model) |
| `EMBEDDING_MODEL` | ✅ Yes | `all-MiniLM-L6-v2` (local) |
| `CHUNK_SIZE` | ⚠️ Optional | Default: `700` |
| `CHUNK_OVERLAP` | ⚠️ Optional | Default: `80` |
| `TOP_K` | ⚠️ Optional | Default: `4` |

---

## 💡 How to Use

1. Upload a PDF using the file uploader at the top
2. Wait for processing (shows pages + chunks count)
3. Ask a question in plain English
4. Get an answer with:
   - The answer text
   - Source file + page number
   - Evidence snippet (expandable)
   - Which model answered + which API key was used

### Example

**Input PDF:** `college_handbook.pdf` (12 pages)

**Question:** "What is the minimum attendance requirement?"

**Output:**

```text
Minimum 75% attendance is required to appear for final exams.

Sources:
1. college_handbook.pdf — page 12

🧠 meta-llama/llama-3.3-70b-instruct | 🔑 key_1
```

---

## 🧪 Testing Methodology

### Manual Evaluation Dataset

For each test PDF, prepare 20–30 questions with known correct answers:

| Test Type | What to Verify |
|-----------|----------------|
| Direct question | Correct answer + correct page |
| Paraphrased question | Same retrieval despite different wording |
| Multi-part question | Answer pulls from multiple chunks |
| Missing info | App says "could not find" instead of guessing |
| Similar topics | Right section retrieved, not a similar one |

### Unit Tests

```bash
pytest tests/ -v
```

Tests cover:

- PDF text extraction (valid + invalid files)
- Chunking (overlap + metadata preservation)
- Retrieval (relevant chunks for known queries)
- RAG pipeline (end-to-end behavior)

### Edge Cases Handled

- ✅ Scanned PDFs (no extractable text) → clear error
- ✅ Empty files → validation error
- ✅ Wrong file types → validation error
- ✅ Oversized files (>20MB) → validation error
- ✅ API key failure → automatic fallback to key 2
- ✅ All keys fail → graceful error message
- ✅ Questions with no answer in PDF → honest fallback

---

## 🔒 Privacy & Security

- PDFs are never uploaded to any server. Text extraction, chunking, and embedding all happen locally.
- Only the retrieved chunks + question are sent to the LLM API (OpenRouter).
- API keys are stored in `.env` (local) and never committed to Git.
- For production deployments, use Streamlit Secrets.

---

## ⚠️ Known Limitations

| Limitation | Reason | Future Fix |
|-----------|--------|------------|
| No OCR | Scanned PDFs have no extractable text | Add Tesseract OCR |
| Single PDF at a time | MVP scope | Multi-document support |
| In-memory index | No persistence | Save FAISS index to disk |
| 50 requests/day per key | OpenRouter free tier | Add $10 credit (1000/day) |
| First query is slow | Model download (~80MB) | Bundle model or cache |
| No user authentication | Public demo | Add OAuth |
| English-only embeddings | all-MiniLM-L6-v2 | Use multilingual model |

---

## 🗺️ Roadmap

### ✅ Level 1 — MVP (Current)

- ☑ Single PDF upload
- ☑ Text extraction + page metadata
- ☑ Chunking + local embeddings
- ☑ FAISS retrieval
- ☑ LLM answer generation
- ☑ Page-level citations
- ☑ No-answer fallback
- ☑ Dark theme UI

### 🚧 Level 2 — Better RAG (Next)

- ☐ Chat history persistence (last 3 chats)
- ☐ Multiple PDFs per session
- ☐ Chunk size + top-k tuning UI
- ☐ 30-question evaluation dataset
- ☐ Retrieval quality metrics

### 🔮 Level 3 — Production

- ☐ FastAPI backend
- ☐ Docker container
- ☐ Persistent document storage
- ☐ User authentication
- ☐ AWS EC2 deployment
- ☐ Logging + monitoring

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

MIT License — see `LICENSE` for details.

---

## 👤 Author

**Amrit Rai**

- LinkedIn: [amrit-rai-data-analyst](https://www.linkedin.com/in/amrit-rai-data-analyst/)
- GitHub: [@amritrai404](https://github.com/amritrai404)

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the rapid UI framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF parsing
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [sentence-transformers](https://www.sbert.net/) for local embeddings
- [OpenRouter](https://openrouter.ai/) for free LLM access

---

## 📸 Screenshots

Coming soon — see the live demo below.

---

## 🔗 Live Demo

Coming soon — will be deployed on Streamlit Community Cloud.

---

⭐ **If you found this useful, please consider starring the repo!**
