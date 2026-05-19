from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

INCIDENTS_DIR = DATA_DIR / "incidents"
LOGS_DIR = DATA_DIR / "logs"
DOCS_DIR = DATA_DIR / "docs"