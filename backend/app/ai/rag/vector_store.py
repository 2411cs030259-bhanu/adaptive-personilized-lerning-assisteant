from __future__ import annotations
from pathlib import Path
import json
import math
from app.core.config import VECTOR_DIR
from app.ai.embeddings.service import embed_text

class LocalVectorStore:
    def __init__(self, path: Path | None = None):
        self.path = path or (VECTOR_DIR / "store.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.items = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else []
        except Exception:
            self.items = []

    def _save(self):
        temp = self.path.with_suffix(".tmp")
        temp.write_text(json.dumps(self.items, ensure_ascii=False), encoding="utf-8")
        temp.replace(self.path)

    def add_documents(self, docs):
        for doc in docs:
            self.items = [x for x in self.items if not (x.get("student_id") == doc.get("student_id") and x.get("chunk_id") == doc.get("chunk_id"))]
            item = dict(doc)
            item["embedding"] = embed_text(item.get("text", "")).tolist()
            self.items.append(item)
        self._save()

    @staticmethod
    def _cosine(a, b):
        da = math.sqrt(sum(x*x for x in a)); db = math.sqrt(sum(x*x for x in b))
        return sum(x*y for x,y in zip(a,b)) / (da*db) if da and db else 0.0

    def search(self, query, k=5):
        qv = embed_text(query.get("query", "")).tolist()
        scored = []
        for item in self.items:
            if item.get("student_id") != query.get("student_id"):
                continue
            score = self._cosine(qv, item.get("embedding", []))
            # Small lexical boost helps exact topic questions.
            q_terms = {w for w in query.get("query", "").lower().split() if len(w) > 2}
            text = item.get("text", "").lower()
            score += 0.08 * sum(1 for term in q_terms if term in text)
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{k:v for k,v in item.items() if k != "embedding"} for _, item in scored[:k]]

    def delete(self, material_id):
        self.items = [d for d in self.items if d.get("material_id") != material_id]
        self._save()

class RAGService:
    def __init__(self):
        self.store = LocalVectorStore()

    def index(self, docs):
        self.store.add_documents(docs)

    def retrieve(self, student_id, question, k=5):
        return self.store.search({"student_id": student_id, "query": question}, k)

    def context(self, chunks):
        return "\n\n".join(f"[{i+1}] {c['text']}" for i,c in enumerate(chunks))

rag = RAGService()
