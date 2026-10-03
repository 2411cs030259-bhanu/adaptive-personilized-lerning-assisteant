from pathlib import Path
import re

def extract_text(path: str):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        try:
            import fitz
        except ImportError as exc:
            raise ValueError("PDF support requires PyMuPDF. Run: pip install -r requirements.txt") from exc
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc), len(doc)
    if ext == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise ValueError("DOCX support requires python-docx. Run: pip install -r requirements.txt") from exc
        d = Document(path)
        return "\n".join(p.text for p in d.paragraphs), None
    if ext == ".txt":
        return Path(path).read_text(encoding="utf-8", errors="ignore"), None
    raise ValueError("Unsupported file type. Upload PDF, DOCX or TXT.")

def clean_text(text: str):
    return re.sub(r"\s+", " ", text.replace("\x00", " ")).strip()

def detect_topics(text: str):
    candidates = [
        "Processes", "CPU Scheduling", "Synchronization", "Deadlocks", "Memory Management",
        "File Systems", "Virtual Memory", "Operating Systems", "Database Management",
        "Data Structures", "Computer Networks", "Java", "Python"
    ]
    compact = text.lower().replace(" ", "")
    found = [x for x in candidates if x.lower().replace(" ", "") in compact]
    return found or ["General Concepts"]

def chunk_text(text: str, size=900, overlap=120):
    words = text.split(); out=[]; start=0; step=max(1, size-overlap)
    while start < len(words):
        out.append(" ".join(words[start:start+size])); start += step
    return out or [""]
