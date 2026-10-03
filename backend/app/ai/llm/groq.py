import json
import httpx
from .base import LLMProvider

class GroqLLM(LLMProvider):
    def __init__(self,key,model): self.key,self.model=key,model
    def _call(self,prompt):
        with httpx.Client(timeout=60) as client:
            response=client.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {self.key}","Content-Type":"application/json"},json={"model":self.model,"messages":[{"role":"system","content":"You are a grounded academic tutor. Use the supplied study context as the factual source. If context is missing, say so."},{"role":"user","content":prompt}],"temperature":0.2})
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    def generate_answer(self,question,context): return self._call(f"Question: {question}\n\nSTUDY CONTEXT:\n{context}\n\nExplain clearly for a college student and cite context items as [1], [2] when applicable.")
    def generate_quiz(self,topic,context,count,difficulty):
        raw=self._call(f"Create exactly {count} MCQs about {topic}. Difficulty: {difficulty}. Use the context below. Return ONLY a JSON array; no markdown. Each object needs question, question_type='mcq', options (4 strings), correct_answer, explanation, topic, difficulty, source_material.\nContext:\n{context}")
        cleaned=raw.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)
