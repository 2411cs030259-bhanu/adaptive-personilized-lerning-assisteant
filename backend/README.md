# Adaptive AI Personal Learning Assistant — Python 3.14 Backend

This folder is a **drop-in replacement for the backend** of the existing Vite/React frontend.

## Frontend contract preserved
The frontend can keep using:
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/students/me`
- `GET /api/materials`
- `POST /api/materials/upload` (`multipart/form-data`, fields: `file`, `subject`)
- `DELETE /api/materials/{id}`
- `POST /api/tutor/ask`
- `POST /api/tutor/summarize`
- `POST /api/quiz/generate`
- `POST /api/quiz/{id}/submit`
- `GET /api/quiz/history`
- `GET /api/progress`
- `GET /api/progress/mastery`
- `GET /api/recommendations`
- `GET /api/recommendations/study-plan`

Authentication is JWT Bearer authentication, matching the frontend interceptor that reads `localStorage.token`.

## Python 3.14
Use Python 3.14. The default install intentionally avoids forcing heavyweight ML packages during first startup. The backend still exposes the AI architecture and can use Groq and Sentence Transformers when configured.

PyTorch currently publishes Python 3.14 support, and the current PyMuPDF and FAISS releases also provide Python 3.14 wheels. The optional transformer stack is therefore isolated rather than imported at startup.

## Run on Windows
Open a terminal **inside this backend folder**:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Health check: `http://127.0.0.1:8000/health`
API docs: `http://127.0.0.1:8000/docs`

Set the frontend `.env` to:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

## Real Groq
Edit `.env`:

```env
LLM_PROVIDER=groq
LLM_API_KEY=your_groq_key
LLM_MODEL=llama-3.3-70b-versatile
```

Without a key, the application remains usable with the clearly labeled Demo Tutor/quiz provider.

## Semantic embeddings
Default `EMBEDDING_PROVIDER=hash` is deterministic and needs no model download. For transformer embeddings:

```powershell
pip install torch sentence-transformers
```

then set:

```env
EMBEDDING_PROVIDER=sentence_transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## DKT
The quiz submission path always updates mastery. `DKT_MODE=demo` uses the explicit deterministic mastery fallback. To execute a compatible trained checkpoint, install the optional PyTorch stack and set `DKT_MODE=trained` plus `MODEL_PATH`.

## Data locations
Everything is inside the backend folder so the backend does not break when launched from another working directory:
- `adaptive_learning.db`
- `storage/uploads/`
- `storage/vectors/store.json`
- `ml_models/dkt/`

## Drop-in replacement
Replace your existing `backend` folder with this folder. Do not change the frontend API file. Start the backend on port `8000` and keep the frontend on port `5173`.
