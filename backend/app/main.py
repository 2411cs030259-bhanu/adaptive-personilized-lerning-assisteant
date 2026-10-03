from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import Base, engine, SessionLocal
from app.database.models import DocumentChunk
from app.ai.rag.service import rag
from app.api import auth, students, materials, tutor, quiz, progress, recommendations

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Rebuild the persistent RAG index from the database after every restart.
    db=SessionLocal()
    try:
        chunks=db.query(DocumentChunk).all()
        rag.index([{"student_id":c.student_id,"material_id":c.material_id,"chunk_id":c.id,"topic":c.topic,"text":c.text} for c in chunks])
    finally:
        db.close()
    yield

app=FastAPI(title="Adaptive AI Personal Learning Assistant",version="2.0.0",lifespan=lifespan)
origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

for router in (auth.router,students.router,materials.router,tutor.router,quiz.router,progress.router,recommendations.router):
    app.include_router(router,prefix=settings.api_prefix)

@app.get("/")
def root(): return {"name":"Adaptive AI Personal Learning Assistant","status":"ok","api":"/api"}

@app.get("/health")
def health(): return {"status":"healthy","python_compatible":"3.14","database":"configured"}
