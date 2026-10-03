from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database.models import Student

_password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return _password_hash.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _password_hash.verify(password, password_hash)
    except Exception:
        return False

def authenticate(db: Session, email: str, password: str):
    student = db.query(Student).filter(Student.email == email.lower()).first()
    return student if student and verify_password(password, student.password_hash) else None

def token_for(student_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": str(student_id), "iat": now, "exp": now + timedelta(minutes=settings.access_token_minutes)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def student_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError) as exc:
        raise ValueError("Invalid or expired token") from exc
