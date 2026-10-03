from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ is the application root. Nothing depends on the terminal's cwd.
BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    database_url: str = f"sqlite:///{(BASE_DIR / 'adaptive_learning.db').as_posix()}"
    jwt_secret: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 720

    llm_provider: str = "demo"  # demo | groq
    llm_api_key: str = ""
    llm_model: str = "llama-3.3-70b-versatile"

    embedding_provider: str = "hash"  # hash | sentence_transformers
    embedding_model: str = "all-MiniLM-L6-v2"
    vector_store: str = "local"

    dkt_mode: str = "demo"  # demo | trained
    model_path: str = str(BASE_DIR / "ml_models" / "dkt" / "best_model.pt")

    max_upload_mb: int = 10
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    api_prefix: str = "/api"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

settings = Settings()

UPLOAD_DIR = BASE_DIR / "storage" / "uploads"
VECTOR_DIR = BASE_DIR / "storage" / "vectors"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)
