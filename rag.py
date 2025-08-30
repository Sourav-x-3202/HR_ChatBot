import os
import re
from typing import List, Dict, Tuple
import numpy as np

try:
    import torch
except Exception:
    torch = None

from sentence_transformers import SentenceTransformer, util

# Google Gemini
try:
    import google.generativeai as genai
except Exception:
    genai = None

from data import EMPLOYEES


def _employee_to_text(emp: Dict) -> str:
    """Convert employee dict into a human-readable string for retrieval."""
    return (
        f"{emp['name']} — {emp['role']} | Skills: {', '.join(emp['skills'])} | "
        f"Experience: {emp['experience_years']} years | Location: {emp['location']} | "
        f"Email: {emp['email']}"
    )


class RAGEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", top_k: int = 5):
        self.model = SentenceTransformer(model_name)
        self.top_k = top_k

        # Precompute corpus embeddings
        self.corpus_texts = [_employee_to_text(emp) for emp in EMPLOYEES]
        self.corpus_embeddings = self.model.encode(
            self.corpus_texts, convert_to_tensor=True, normalize_embeddings=True
        )

        # Gemini config
        self.api_key = os.getenv("GEMINI_API_KEY", "YOUR_PASTED_GEMINI_API_KEY_HERE")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self._configure_gemini()

    def _configure_gemini(self):
        if genai is None:
            self.gemini = None
            return
        try:
            genai.configure(api_key=self.api_key)
            self.gemini = genai.GenerativeModel(self.gemini_model)
        except Exception:
            self.gemini = None

    def _structured_filter(self, query: str) -> List[int]:
        """
        Filter employees based on explicit mentions of role, skills, location.
        Hybrid approach: structured + semantic.
        """
        query_lower = re.sub(r"[^a-z0-9\s\+\#\.]", " ", query.lower())

        required_roles = []
        if "frontend" in query_lower:
            required_roles.append("frontend")
        if "backend" in query_lower:
            required_roles.append("backend")
        if "data scientist" in query_lower:
            required_roles.append("data scientist")
        if "ml engineer" in query_lower:
            required_roles.append("ml engineer")

        required_skills = []
        for token in ["python", "react", "next.js", "docker", "aws", "kubernetes", "java", "graphql"]:
            if token in query_lower:
                required_skills.append(token)

        required_location = None
        for loc in ["bengaluru", "delhi", "hyderabad", "mumbai", "remote"]:
            if loc in query_lower:
                required_location = loc

        filtered = []
        for idx, emp in enumerate(EMPLOYEES):
            match = True

            # Role filter
            if required_roles:
                if not any(r in emp["role"].lower() for r in required_roles):
                    match = False

            # Skill filter (must contain ALL mentioned skills)
            if required_skills:
                emp_skills = [s.lower() for s in emp["skills"]]
                if not all(any(req in s for s in emp_skills) for req in required_skills):
                    match = False

            # Location filter
            if required_location:
                if required_location not in emp["location"].lower():
                    match = False

            if match:
                filtered.append(idx)

        return filtered

    def retrieve(self, query: str) -> List[Tuple[int, float]]:
        """Hybrid retrieval: first structured filtering, then semantic ranking."""
        structured_idxs = self._structured_filter(query)

        query_emb = self.model.encode(query, convert_to_tensor=True, normalize_embeddings=True)

        if structured_idxs:
            subset_embeddings = [self.corpus_embeddings[i] for i in structured_idxs]
            subset_embeddings = torch.stack(subset_embeddings)
            scores = util.cos_sim(query_emb, subset_embeddings)[0]
            top_k = min(self.top_k, len(structured_idxs))
            top_results = torch.topk(scores, k=top_k)
            idxs = [structured_idxs[i] for i in top_results.indices.cpu().tolist()]
            vals = top_results.values.cpu().tolist()
        else:
            # fallback semantic
            scores = util.cos_sim(query_emb, self.corpus_embeddings)[0]
            top_k = min(self.top_k, len(self.corpus_texts))
            top_results = torch.topk(scores, k=top_k)
            idxs = top_results.indices.cpu().tolist()
            vals = top_results.values.cpu().tolist()

        # Deduplicate results (avoid repeated employees)
        seen = set()
        unique_idxs, unique_vals = [], []
        for i, v in zip(idxs, vals):
            if i not in seen:
                seen.add(i)
                unique_idxs.append(i)
                unique_vals.append(v)

        return list(zip(unique_idxs, unique_vals))

    def generate(self, query: str, retrieved_indices: List[int]) -> str:
        """Generate response using Gemini or fallback formatting."""
        context_lines = [self.corpus_texts[i] for i in retrieved_indices]
        context_block = "\n".join(f"- {line}" for line in context_lines)

        system_prompt = (
            "You are an HR assistant chatbot. Answer ONLY from the provided employee context. "
            "If nothing matches, say 'No employees found'. Be concise."
        )
        user_prompt = (
            f"User query: {query}\n\n"
            f"Employee context:\n{context_block}\n\n"
            "Return a short, clear list of matching employees."
        )

        if self.gemini is not None and self.api_key and "YOUR_PASTED" not in self.api_key:
            try:
                resp = self.gemini.generate_content([system_prompt, user_prompt])
                return resp.text.strip()
            except Exception:
                pass

        # Fallback
        if not retrieved_indices:
            return "No employees found."

        lines = ["Here are matching employees:"]
        for i in retrieved_indices:
            lines.append(f"- {self.corpus_texts[i]}")
        return "\n".join(lines)

    def answer(self, query: str) -> Dict:
        """End-to-end pipeline: retrieve + generate response."""
        matches = self.retrieve(query)
        idxs = [i for i, _ in matches]
        answer_text = self.generate(query, idxs)
        matched_emps = [EMPLOYEES[i] for i in idxs]
        scores = [float(s) for _, s in matches]
        return {"response": answer_text, "employees": matched_emps, "scores": scores}
