
# HR Resource Query Chatbot

[![Python](https://img.shields.io/badge/python-3.10%20--%203.13-blue)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-FF4B4B?logo=streamlit)](https://streamlit.io/)  
[![Torch](https://img.shields.io/badge/PyTorch-2.6+-EE4C2C?logo=pytorch)](https://pytorch.org/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

An intelligent **HR assistant chatbot** that helps you query employee data in **natural language**.  
It combines **semantic retrieval** with **LLM-powered generation** using a hybrid **RAG (Retrieval-Augmented Generation)** approach.  

With this tool, you can ask:  
- *"Show me backend developers in Bengaluru with 5+ years of experience"*  
- *"Who are the UI/UX designers skilled in Figma?"*  
- *"List employees with leadership roles in sales"*  

and get **chat-style responses** with matching employee details.   

---

##  Features

-  **Semantic Search** → Search employees by role, skills, experience, and location.  
-  **Conversational Chat** → Ask questions in plain English.  
-  **FastAPI Backend** → Exposes REST endpoints for integration.  
-  **Streamlit Frontend** → Interactive chat-like interface.  
-  **Hybrid RAG Engine** → Combines embeddings (`sentence-transformers`) with **Gemini LLM** for contextual answers.  
-  **Extendable Dataset** → Add/update employees in `data.py` or link to your HR database.  
-  **Fallback Mode** → Even without Gemini API, retrieval still works.  

---

##  System Architecture

<img width="768" height="101" alt="hr_chatbot_architecture" src="https://github.com/user-attachments/assets/49cc0887-96bf-43c9-9931-55dddf98e70c" />


---

## Project Structure

```bash
HR_ChatBot/
│── 📜 app.py             # Streamlit frontend (chat interface)
│── 📜 main.py            # FastAPI backend (API endpoints)
│── 📜 rag.py             # RAG engine (semantic search + LLM)
│── 📜 data.py            # Employee seed dataset
│── 📜 requirements.txt   # Python dependencies
│── 📜 README.md          # Project documentation
│
└── 📂 assets/            # (Optional) Screenshots & demo images
    ├── ui_demo.png
    └── architecture.png
```
---

##  Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/HR_ChatBot.git
cd HR_ChatBot
```
### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt

```
---
## Configure Gemini API

Obtain an API key from Google AI Studio.
Set it as an environment variable:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="YOUR_KEY"

# macOS/Linux
export GEMINI_API_KEY="YOUR_KEY"

```
If no key is set, the chatbot falls back to *retrieval-only answers*.

---

## Run the App
### Start Backend (FastAPI)

```bash
uvicorn main:app --reload
```
- Open API docs → http://localhost:8000/docs

### Start Frontend (Streamlit)  

```bash
streamlit run app.py

```
- UI runs at → http://localhost:8501
-Update Backend URL in the UI if backend is running elsewhere.

---

## Screenshots
**Chat UI** (Streamlit)
<img width="2555" height="1304" alt="Screenshot 2025-08-31 044950" src="https://github.com/user-attachments/assets/af3923ea-bb0a-4e66-8e34-65730406405e" />

**Employee Search Result**
<img width="2555" height="1362" alt="Screenshot 2025-08-31 045109" src="https://github.com/user-attachments/assets/3310b6cf-2e37-4e0e-887d-edd5aa3a4650" />

---

## Employee Dataset
- Seed data is in data.py.
- Each employee contains:
```python
{
  "id": 1,
  "name": "Alice Johnson",
  "role": "Backend Developer",
  "skills": ["Python", "Django", "PostgreSQL"],
  "experience": 5,
  "location": "Bengaluru"
}
```
- Extendable: Replace with CSV, DB, or API integration.
---

## Notes

- Works with Python 3.10 – 3.13.
- For Python 3.13, use PyTorch ≥ 2.6.0.
- For GPU users, install CUDA-enabled PyTorch manually:
```powershell
# Example for CUDA 12.1 on Windows
pip install torch --index-url https://download.pytorch.org/whl/cu121
```
- If Gemini API is down, app gracefully falls back to retrieval answers.

---

## Contributing

Want to improve this project? Contributions are welcome!

- Fork the repo
- Create your feature branch → git checkout -b feature/my-feature
- Commit changes → git commit -m "Add my feature"
- Push branch → git push origin feature/my-feature
- Open a Pull Request

---
## Author

**Sourav Sharma**
Developer. Maker. Privacy-first AI enthusiast.
Find me on GitHub → [@Sourav-x-3202](https://github.com/Sourav-x-3202)

---


## Star This Project

If you found this useful, helpful, or inspiring — please consider starring the repository.
It helps others discover the project and keeps development going 

---
## License

This project is licensed under the MIT License.
© 2025 Sourav Sharma

