from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "/api/auth/register", "/api/auth/login", "/api/students/me",
    "/api/materials", "/api/materials/upload", "/api/tutor/ask",
    "/api/tutor/summarize", "/api/quiz/generate", "/api/progress",
    "/api/recommendations",
]

def test_project_is_self_contained():
    assert (ROOT / "app" / "main.py").exists()
    assert (ROOT / "requirements.txt").exists()
    assert (ROOT / "run.bat").exists()

def test_frontend_contract_is_documented():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for route in EXPECTED:
        assert route in readme
