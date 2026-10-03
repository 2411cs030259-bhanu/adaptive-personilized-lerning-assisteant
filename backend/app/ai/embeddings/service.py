from __future__ import annotations
import hashlib
import numpy as np
from app.core.config import settings

_model = None

# 384 dimensions keeps the fallback lightweight while remaining deterministic.
HASH_DIM = 384

def _hash_embedding(text: str) -> np.ndarray:
    v = np.zeros(HASH_DIM, dtype=np.float32)
    words = text.lower().split()
    for i, word in enumerate(words):
        digest = hashlib.sha256(word.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "little") % HASH_DIM
        v[idx] += 1.0 + (i % 7) * 0.01
    norm = np.linalg.norm(v)
    return v / norm if norm else v

def embed_texts(texts, model_name=None):
    global _model
    model_name = model_name or settings.embedding_model
    if settings.embedding_provider.lower() == "sentence_transformers":
        try:
            if _model is None:
                from sentence_transformers import SentenceTransformer
                _model = SentenceTransformer(model_name)
            return np.asarray(_model.encode(texts, normalize_embeddings=True), dtype="float32")
        except Exception:
            # Keep the API usable on Python 3.14 machines without optional ML wheels/model downloads.
            pass
    return np.asarray([_hash_embedding(t) for t in texts], dtype="float32")

def embed_text(text, model_name=None):
    return embed_texts([text], model_name)[0]
