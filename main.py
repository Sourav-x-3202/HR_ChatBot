from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any

from rag import RAGEngine

app = FastAPI(title="HR Resource Query Chatbot API", version="1.0.0")

# CORS for local Streamlit / web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RAGEngine()


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(req: ChatRequest) -> Dict[str, Any]:
    return engine.answer(req.query)


@app.get("/employees/search")
def employees_search(query: str = Query(..., description="Natural language search over employees")) -> Dict[str, Any]:
    result = engine.answer(query)
    return {"employees": result["employees"], "scores": result["scores"]}


# ---------------------------
# Serve the UI at "/"
# ---------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>HR Resource Chatbot</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 flex items-center justify-center min-h-screen">
  <div class="bg-white shadow-xl rounded-2xl p-6 w-full max-w-3xl">
    <h1 class="text-2xl font-bold text-center mb-6 text-blue-600">💼 HR Resource Chatbot</h1>

    <!-- Chat Section -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold mb-2">Chat with HR Bot</h2>
      <div id="chatBox" class="h-64 overflow-y-auto border border-gray-200 rounded-lg p-3 mb-3 bg-gray-50"></div>
      <div class="flex">
        <input id="chatInput" type="text" placeholder="Type your question..." class="flex-1 p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-400">
        <button onclick="sendChat()" class="px-4 py-2 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700">Send</button>
      </div>
    </div>

    <!-- Employee Search Section -->
    <div>
      <h2 class="text-lg font-semibold mb-2">Search Employees</h2>
      <div class="flex mb-3">
        <input id="searchInput" type="text" placeholder="e.g., Find all developers in HR" class="flex-1 p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-green-400">
        <button onclick="searchEmployees()" class="px-4 py-2 bg-green-600 text-white rounded-r-lg hover:bg-green-700">Search</button>
      </div>
      <div id="searchResults" class="border border-gray-200 rounded-lg p-3 bg-gray-50"></div>
    </div>
  </div>

  <script>
    async function sendChat() {
      const input = document.getElementById('chatInput');
      const chatBox = document.getElementById('chatBox');
      const query = input.value.trim();
      if (!query) return;

      chatBox.innerHTML += `<div class='text-right mb-2'><span class='bg-blue-100 text-blue-800 px-3 py-1 rounded-lg inline-block'>${query}</span></div>`;
      input.value = "";

      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });
      const data = await res.json();

      chatBox.innerHTML += `<div class='text-left mb-2'><span class='bg-gray-200 px-3 py-1 rounded-lg inline-block'>${data.answer || JSON.stringify(data)}</span></div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function searchEmployees() {
      const query = document.getElementById('searchInput').value.trim();
      if (!query) return;

      const res = await fetch(`/employees/search?query=${encodeURIComponent(query)}`);
      const data = await res.json();

      document.getElementById('searchResults').innerHTML = `
        <pre class="whitespace-pre-wrap text-sm">${JSON.stringify(data, null, 2)}</pre>
      `;
    }
  </script>
</body>
</html>
    """
