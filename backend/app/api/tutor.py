from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Student
from app.api.deps import current_student
from app.schemas.tutor import TutorAsk,TutorResponse
from app.ai.rag.service import rag
from app.ai.llm.service import provider
router=APIRouter(prefix="/tutor",tags=["tutor"])
@router.post("/ask",response_model=TutorResponse)
def ask(x:TutorAsk,db:Session=Depends(get_db),s:Student=Depends(current_student)):
    chunks=rag.retrieve(s.id,x.question,5);ctx=rag.context(chunks);p=provider();answer=p.generate_answer(x.question,ctx)
    return {"answer":answer,"sources":[f"{c['topic']} · material #{c['material_id']}" for c in chunks],"mode":"demo" if p.__class__.__name__=="DemoLLM" else "llm"}
@router.post("/summarize")
def summarize(x:TutorAsk,db:Session=Depends(get_db),s:Student=Depends(current_student)):
    chunks=rag.retrieve(s.id,x.question,5);return {"answer":provider().generate_answer("Summarize this topic: "+x.question,rag.context(chunks))}
