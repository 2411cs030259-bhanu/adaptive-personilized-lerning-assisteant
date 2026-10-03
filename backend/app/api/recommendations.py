from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Student,KnowledgeState,QuizAttempt
from app.api.deps import current_student
from app.recommendation.adaptive_difficulty import choose_difficulty
from app.recommendation.study_plan import make_plan
router=APIRouter(prefix="/recommendations",tags=["recommendations"])
@router.get("")
def recommendations(db:Session=Depends(get_db),s:Student=Depends(current_student)):
    states=db.query(KnowledgeState).filter(KnowledgeState.student_id==s.id).all()
    if not states: states=[KnowledgeState(topic="Deadlock Prevention",mastery=.42),KnowledgeState(topic="Synchronization",mastery=.56)]
    states=sorted(states,key=lambda x:x.mastery);weak=[{"topic":x.topic,"mastery":x.mastery} for x in states if x.mastery<.6]
    target=states[0]; attempts=db.query(QuizAttempt).filter(QuizAttempt.student_id==s.id).order_by(QuizAttempt.timestamp.desc()).limit(5).all()
    recent=sum(1 for x in attempts if x.correct)/len(attempts) if attempts else .6
    diff=choose_difficulty(target.mastery,recent)
    return {"current_topic":target.topic,"overall_mastery":round(sum(x.mastery for x in states)/len(states)*100),"weak_topics":[{"topic":x.topic,"mastery":round(x.mastery*100)} for x in states if x.mastery<.6],"recommended_practice":{"topic":target.topic,"difficulty":diff,"questions":5},"recommendations":[{"title":f"Review {target.topic}","reason":f"Your estimated mastery is {round(target.mastery*100)}% and your recent performance is below your target."},{"title":f"Practice 5 {diff} questions","reason":"The difficulty is selected from your recent performance and estimated mastery."},{"title":"Review Synchronization","reason":"Continue strengthening the next lowest developing topic."}]}
@router.get("/study-plan")
def study_plan(db:Session=Depends(get_db),s:Student=Depends(current_student)):
    states=db.query(KnowledgeState).filter(KnowledgeState.student_id==s.id).all()
    weak=[{"topic":x.topic} for x in sorted(states,key=lambda x:x.mastery)] or [{"topic":"Deadlocks"},{"topic":"Synchronization"}]
    return make_plan(weak)
