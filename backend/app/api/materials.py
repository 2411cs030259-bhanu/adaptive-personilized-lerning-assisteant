from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Student, Material, Topic, DocumentChunk
from app.api.deps import current_student
from app.core.config import settings, UPLOAD_DIR
from app.document_processing.extractor import extract_text, clean_text, detect_topics, chunk_text
from app.ai.rag.service import rag

router = APIRouter(prefix="/materials", tags=["materials"])

@router.post("/upload")
def upload(file: UploadFile = File(...), subject: str = Form("General"), db: Session = Depends(get_db), s: Student = Depends(current_student)):
    original = Path(file.filename or "material.txt").name
    ext = Path(original).suffix.lower()
    if ext not in {".pdf", ".docx", ".txt"}:
        raise HTTPException(400, "Unsupported format. Upload PDF, DOCX or TXT.")
    data = file.file.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File is larger than {settings.max_upload_mb} MB.")
    stored = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
    stored.write_bytes(data)
    try:
        raw, _ = extract_text(str(stored)); text = clean_text(raw); topics = detect_topics(text)
    except Exception as exc:
        stored.unlink(missing_ok=True)
        raise HTTPException(400, str(exc))

    material = Material(student_id=s.id, filename=original, subject=subject.strip() or "General", path=str(stored), status="processed")
    db.add(material); db.flush()
    docs=[]
    for i, chunk in enumerate(chunk_text(text)):
        topic = topics[min(i, len(topics)-1)]
        c = DocumentChunk(student_id=s.id, material_id=material.id, topic=topic, text=chunk)
        db.add(c); db.flush()
        docs.append({"student_id": s.id, "material_id": material.id, "chunk_id": c.id, "topic": topic, "text": chunk})
        if not db.query(Topic).filter(Topic.student_id==s.id, Topic.name==topic, Topic.subject==material.subject).first():
            db.add(Topic(student_id=s.id, name=topic, subject=material.subject))
    db.commit(); rag.index(docs)
    return {"id": material.id, "filename": original, "subject": material.subject, "status": "processed", "topics": topics}

@router.get("")
def materials(db: Session = Depends(get_db), s: Student = Depends(current_student)):
    rows = db.query(Material).filter(Material.student_id==s.id).order_by(Material.created_at.desc()).all()
    out=[]
    for m in rows:
        topics=[x.name for x in db.query(DocumentChunk).filter(DocumentChunk.student_id==s.id, DocumentChunk.material_id==m.id).distinct().all()]
        out.append({"id":m.id,"filename":m.filename,"subject":m.subject,"status":m.status,"topics":topics})
    return out

@router.delete("/{material_id}")
def delete(material_id:int, db:Session=Depends(get_db), s:Student=Depends(current_student)):
    material=db.query(Material).filter(Material.id==material_id,Material.student_id==s.id).first()
    if not material: raise HTTPException(404,"Material not found")
    Path(material.path).unlink(missing_ok=True)
    db.delete(material); db.commit(); rag.store.delete(material_id)
    return {"ok":True}
