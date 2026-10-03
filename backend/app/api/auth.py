from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Student
from app.schemas.auth import RegisterRequest, LoginRequest, StudentOut
from app.services.auth_service import hash_password, authenticate, token_for

router = APIRouter(prefix="/auth", tags=["auth"])

def _student_response(student: Student):
    return {"access_token": token_for(student.id), "token_type": "bearer", "student": StudentOut.model_validate(student)}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(x: RegisterRequest, db: Session = Depends(get_db)):
    email = str(x.email).lower()
    if db.query(Student).filter(Student.email == email).first():
        raise HTTPException(409, "Email already registered")
    student = Student(
        name=x.name.strip(), email=email, password_hash=hash_password(x.password),
        course=x.course.strip() or "Computer Science", semester=str(x.semester).strip() or "6",
    )
    db.add(student); db.commit(); db.refresh(student)
    return _student_response(student)

@router.post("/login")
def login(x: LoginRequest, db: Session = Depends(get_db)):
    student = authenticate(db, str(x.email).lower(), x.password)
    if not student:
        raise HTTPException(401, "Incorrect email or password")
    return _student_response(student)
