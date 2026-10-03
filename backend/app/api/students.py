from fastapi import APIRouter,Depends
from app.api.deps import current_student
from app.database.models import Student
from app.schemas.auth import StudentOut
router=APIRouter(prefix="/students",tags=["students"])
@router.get("/me",response_model=StudentOut)
def me(s:Student=Depends(current_student)): return s
