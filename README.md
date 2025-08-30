# HR Resource Query Chatbot

An intelligent HR assistant that answers natural-language questions about employee resources using a hybrid **RAG** approach.

## Architecture
- **FastAPI** backend (`main.py`) exposes:
  - `POST /chat` → returns a conversational answer + matched employees
  - `GET /employees/search?query=...` → returns matched employees (raw)
- **RAG Core** (`rag.py`) performs semantic retrieval with `sentence-transformers` and generates the final reply using **Gemini** (`google-generativeai`).
- **Streamlit** UI (`app.py`) provides a simple chat-like interface.

## Setup

> Works on Python **3.10–3.13**. For Python 3.13, PyTorch wheels start at **2.6.0+** (this project specifies `torch>=2.6.0`).

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

### Configure Gemini
Obtain an API key from Google AI Studio and set it before starting the backend:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "YOUR_KEY"
# macOS/Linux
export GEMINI_API_KEY="YOUR_KEY"
```

## Run

**Backend (FastAPI)**
```bash
uvicorn main:app --reload
```
Open API docs at http://localhost:8000/docs

**Frontend (Streamlit)**
```bash
streamlit run app.py
```
If your backend runs elsewhere, update the "Backend URL" box in the UI.

## Notes
- Employee seed data is in `data.py`. Extend it with your org's records.
- If GEMINI is not configured, the app falls back to a simple list-style response so you can still test retrieval.
- For GPU users, install a CUDA build of PyTorch appropriate for your system.
```powershell
# Example for CUDA 12.1 on Windows
pip install torch --index-url https://download.pytorch.org/whl/cu121
```
