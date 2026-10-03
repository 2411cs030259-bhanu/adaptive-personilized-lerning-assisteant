# Adaptive AI Personal Learning Assistant

A final-year-project-ready adaptive learning platform implementing:

**Learn → Practice → Analyze → Identify Weakness → Recommend → Practice Again → Update Knowledge**

The application combines React/Vite/Tailwind, FastAPI, SQLAlchemy/PostgreSQL, document processing, RAG, Sentence Transformers, configurable LLMs, and an LSTM-based Deep Knowledge Tracing (DKT) component.

## What is custom vs pretrained

- **Our custom deep-learning contribution:** LSTM-based Deep Knowledge Tracing.
- **Pretrained:** Sentence Transformer embeddings and the configured LLM.
- **Architecture:** RAG pipeline, vector-store abstraction, recommendation engine and adaptive difficulty.
- **Personalization:** DKT mastery + recent performance + rules/prerequisites.

The DKT service has `demo` mode so the whole application remains usable without model weights. Demo mastery is explicitly labeled as demo/fallback behavior and is not presented as a trained DKT prediction.

## Project structure

```text
adaptive-ai-learning-assistant/
├── frontend/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── ai/
│   │   │   ├── llm/
│   │   │   ├── embeddings/
│   │   │   └── rag/
│   │   ├── ml/
│   │   │   └── dkt/
│   │   ├── document_processing/
│   │   ├── recommendation/
│   │   ├── database/
│   │   ├── schemas/
│   │   └── core/
│   └── requirements.txt
├── ml_models/dkt/
├── data/raw/
├── data/processed/
├── data/sample_materials/
├── storage/
├── notebooks/
├── tests/backend/
├── tests/frontend/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── vercel.json
└── README.md
```

## 1. Local setup

### Backend

Python 3.11 or 3.12 is recommended.

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

### Database

For the easiest local run, the backend defaults to SQLite if `DATABASE_URL` is empty. For the specified production architecture, set:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/adaptive_learning
```

Docker is optional:

```bash
docker compose up -d postgres
```

## 2. Environment variables

See `backend/.env.example` and `frontend/.env.example`.

Important values:

- `DATABASE_URL` — PostgreSQL URL for production; SQLite is convenient for local UI testing.
- `JWT_SECRET` — authentication secret.
- `LLM_PROVIDER` — `demo` or `groq`.
- `LLM_API_KEY` — provider key; never put this in React.
- `LLM_MODEL` — model name.
- `EMBEDDING_MODEL` — Sentence Transformer model.
- `VECTOR_STORE` — `simple` or `faiss`.
- `DKT_MODE` — `demo` or `trained`.
- `MODEL_PATH` — trained DKT checkpoint path.
- `STORAGE_PROVIDER` — `local` or `external`.
- `CORS_ORIGINS` — allowed frontend origins.

## 3. AI Tutor / RAG

Material text is extracted, cleaned, topic-tagged, chunked and embedded. The RAG layer retrieves chunks belonging to the authenticated student's materials before calling the LLM.

The vector store is behind an interface:

```text
add_documents()
search()
delete()
```

The default simple store is JSON-backed and works without a separate vector server. FAISS can be enabled when its deployment environment supports persistence.

If no LLM key exists, the application uses a clearly labeled **Demo Tutor** response.

## 4. Supported material formats

Version 1 supports:

- PDF — PyMuPDF
- DOCX — python-docx
- TXT — standard file handling

PPT/PPTX is intentionally not supported in Version 1.

## 5. Quiz system

Quiz generation uses structured Pydantic validation. The demo provider generates deterministic questions from available topics; the Groq provider can generate structured JSON when configured.

Each interaction records:

- student
- question
- topic
- difficulty
- correctness
- time
- attempt number
- timestamp

## 6. DKT

### Training

The DKT training code is separated from production inference:

```text
ASSISTments
  -> preprocessing
  -> sequence creation
  -> LSTM-DKT
  -> training
  -> evaluation
  -> ml_models/dkt/best_model.pt
```

The training implementation expects a normalized CSV with columns such as:

```text
student_id, question_id, topic_id, correct
```

Run:

```bash
python -m app.ml.dkt.train --data path/to/assistments.csv --output ../../ml_models/dkt/best_model.pt
```

Evaluate:

```bash
python -m app.ml.dkt.evaluate --data path/to/assistments.csv --model ../../ml_models/dkt/best_model.pt
```

Production requests never train the model.

If the checkpoint is absent, set:

```env
DKT_MODE=demo
```

Demo mode is a simple deterministic mastery estimator for UI/testing only.

## 7. Acceptance workflow

1. Start backend.
2. Start frontend.
3. Register.
4. Login.
5. Upload the included sample material.
6. Open Materials and inspect detected topics.
7. Ask the AI Tutor a question.
8. Confirm RAG sources appear.
9. Generate a practice quiz.
10. Complete it.
11. Inspect the result and explanations.
12. Check My Progress.
13. See mastery, weak topics and recommendations update.
14. Use Quick Practice / Continue Learning.
15. Configure a real LLM and trained DKT later without changing the UI flow.

## 8. Vercel

The repository includes `vercel.json` and a serverless-compatible FastAPI entrypoint. For local development, run the FastAPI server from the `backend/` directory; storage paths are resolved back to the repository root.

Production considerations:

- use managed PostgreSQL;
- use durable object storage for uploads;
- use a persistent vector database or durable vector storage;
- do not rely on Vercel's temporary filesystem;
- configure all secrets in Vercel Environment Variables;
- keep the same application modules and API contracts.

The storage abstraction is deliberately used by the material service so a production storage provider can replace local files.

## 9. Security

- passwords are hashed with PBKDF2 via `pwdlib`;
- JWT protected routes;
- Pydantic validation;
- upload extension and size checks;
- SQLAlchemy parameterization;
- API keys remain backend-only;
- generic frontend error messages do not expose stack traces.

## 10. Testing

Backend tests:

```bash
cd backend
pytest
```

Frontend tests:

```bash
cd frontend
npm run test
```

## 11. Future scope

Voice tutor, multilingual learning, Telugu/Hindi support, handwritten-note recognition, image/diagram understanding, coding tutor, AI flashcards, spaced repetition, previous-year paper analysis, AI mock exams, exam-readiness prediction, teacher/parent dashboards, advanced gamification, reminders, Socratic tutoring, knowledge graph, emotion-aware learning and reinforcement-learning-based tutoring are documented future work, not Version 1 features.
