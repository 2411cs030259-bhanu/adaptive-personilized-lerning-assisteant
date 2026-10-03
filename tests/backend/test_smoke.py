from pathlib import Path
def test_project_files_exist():
    assert Path("backend/app/main.py").exists()
    assert Path("frontend/package.json").exists()
