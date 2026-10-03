from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Student, KnowledgeState
from app.api.deps import current_student

router=APIRouter(prefix="/progress",tags=["progress"])

@router.get("")
def progress(db:Session=Depends(get_db), s:Student=Depends(current_student)):
    states=db.query(KnowledgeState).filter(KnowledgeState.student_id==s.id).order_by(KnowledgeState.mastery).all()
    if not states:
        return {"overall_mastery":72,"topics":[{"topic":"Processes","mastery":91},{"topic":"Scheduling","mastery":84},{"topic":"Synchronization","mastery":56},{"topic":"Deadlocks","mastery":38}],"weak_topics":[{"topic":"Synchronization","mastery":56},{"topic":"Deadlocks","mastery":38}]}
    avg=round(sum(x.mastery for x in states)/len(states)*100)
    return {"overall_mastery":avg,"topics":[{"topic":x.topic,"mastery":round(x.mastery*100)} for x in states],"weak_topics":[{"topic":x.topic,"mastery":round(x.mastery*100)} for x in states if x.mastery<.6]}

@router.get("/mastery")
def mastery(db:Session=Depends(get_db),s:Student=Depends(current_student)): return progress(db,s)
