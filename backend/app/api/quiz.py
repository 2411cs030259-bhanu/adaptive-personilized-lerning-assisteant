import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Student, Quiz, Question, QuizQuestion, QuizAttempt, KnowledgeState
from app.api.deps import current_student
from app.schemas.quiz import QuizGenerate, QuizSubmit
from app.ai.rag.service import rag
from app.ai.llm.service import provider
from app.ml.dkt.predict import predict_mastery

router=APIRouter(prefix="/quiz",tags=["quiz"])

@router.post("/generate")
def generate(x:QuizGenerate,db:Session=Depends(get_db),s:Student=Depends(current_student)):
    difficulty=x.difficulty
    if difficulty=="adaptive": difficulty="medium"
    chunks=rag.retrieve(s.id,x.topic,8)
    items=provider().generate_quiz(x.topic,rag.context(chunks),x.number_of_questions,difficulty)
    if not isinstance(items,list) or not items: raise HTTPException(502,"Quiz generator returned no questions")
    qz=Quiz(student_id=s.id,topic=x.topic,difficulty=difficulty); db.add(qz); db.flush(); out=[]
    for item in items[:x.number_of_questions]:
        options=item.get("options",[])
        if not isinstance(options,list) or len(options)<2: continue
        q=Question(topic=item.get("topic",x.topic),difficulty=item.get("difficulty",difficulty),question=str(item["question"]),options_json=json.dumps(options),correct_answer=str(item["correct_answer"]),explanation=str(item.get("explanation","")))
        db.add(q); db.flush(); db.add(QuizQuestion(quiz_id=qz.id,question_id=q.id))
        out.append({"id":q.id,"question":q.question,"options":options,"topic":q.topic,"difficulty":q.difficulty})
    if not out: db.rollback(); raise HTTPException(502,"Quiz generator returned invalid questions")
    db.commit(); return {"id":qz.id,"topic":x.topic,"difficulty":difficulty,"questions":out}

@router.post("/{quiz_id}/submit")
def submit(quiz_id:int,x:QuizSubmit,db:Session=Depends(get_db),s:Student=Depends(current_student)):
    quiz=db.query(Quiz).filter(Quiz.id==quiz_id,Quiz.student_id==s.id).first()
    if not quiz: raise HTTPException(404,"Quiz not found")
    allowed={qq.question_id for qq in db.query(QuizQuestion).filter(QuizQuestion.quiz_id==quiz.id).all()}
    correct=0; feedback=[]; touched_topics=set()
    for answer in x.answers:
        if answer.question_id not in allowed: continue
        q=db.get(Question,answer.question_id)
        if not q: continue
        ok=answer.answer.strip().lower()==q.correct_answer.strip().lower()
        correct += int(ok); touched_topics.add(q.topic)
        db.add(QuizAttempt(student_id=s.id,quiz_id=quiz.id,question_id=q.id,topic=q.topic,difficulty=q.difficulty,correct=ok,time_taken=max(0,answer.time_taken)))
        feedback.append({"question_id":q.id,"correct":ok,"explanation":q.explanation})
    total=len(feedback); pct=round(correct/total*100) if total else 0
    for topic in touched_topics:
        hist=[a.correct for a in db.query(QuizAttempt).filter(QuizAttempt.student_id==s.id,QuizAttempt.topic==topic).order_by(QuizAttempt.timestamp.desc()).limit(20).all()]
        ks=db.query(KnowledgeState).filter(KnowledgeState.student_id==s.id,KnowledgeState.topic==topic).first()
        if not ks: ks=KnowledgeState(student_id=s.id,topic=topic); db.add(ks)
        ks.mastery=predict_mastery(topic,hist)
    db.commit()
    return {"score":correct,"total":total,"percentage":pct,"correct":correct,"incorrect":total-correct,"feedback":feedback}

@router.get("/history")
def history(db:Session=Depends(get_db),s:Student=Depends(current_student)):
    rows=db.query(QuizAttempt).filter(QuizAttempt.student_id==s.id).order_by(QuizAttempt.timestamp.desc()).limit(30).all()
    return [{"topic":r.topic,"correct":r.correct,"time_taken":r.time_taken,"timestamp":r.timestamp} for r in rows]
