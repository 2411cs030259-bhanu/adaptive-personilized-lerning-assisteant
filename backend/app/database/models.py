from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .session import Base

def utcnow():
    return datetime.now(timezone.utc)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    course: Mapped[str] = mapped_column(String(120), default="Computer Science")
    semester: Mapped[str] = mapped_column(String(30), default="6")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))

class Material(Base):
    __tablename__ = "materials"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    filename: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(120), default="General")
    path: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(40), default="processed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(160))
    subject: Mapped[str] = mapped_column(String(120))

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id", ondelete="CASCADE"))
    topic: Mapped[str] = mapped_column(String(160), default="General")
    chapter: Mapped[str] = mapped_column(String(160), default="")
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    text: Mapped[str] = mapped_column(Text)

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String(160))
    difficulty: Mapped[str] = mapped_column(String(30), default="medium")
    question: Mapped[str] = mapped_column(Text)
    options_json: Mapped[str] = mapped_column(Text, default="[]")
    correct_answer: Mapped[str] = mapped_column(String(500))
    explanation: Mapped[str] = mapped_column(Text, default="")

class Quiz(Base):
    __tablename__ = "quizzes"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    topic: Mapped[str] = mapped_column(String(160))
    difficulty: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    __table_args__ = (UniqueConstraint("quiz_id", "question_id", name="uq_quiz_question"),)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    topic: Mapped[str] = mapped_column(String(160))
    difficulty: Mapped[str] = mapped_column(String(30))
    correct: Mapped[bool] = mapped_column(Boolean)
    time_taken: Mapped[float] = mapped_column(Float, default=0)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class KnowledgeState(Base):
    __tablename__ = "knowledge_states"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    topic: Mapped[str] = mapped_column(String(160))
    mastery: Mapped[float] = mapped_column(Float, default=.5)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    __table_args__ = (UniqueConstraint("student_id", "topic", name="uq_student_topic"),)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    topic: Mapped[str] = mapped_column(String(160))
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class StudyPlan(Base):
    __tablename__ = "study_plans"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    plan_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
