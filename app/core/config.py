from pathlib import Path


BASE_DIR = Path("data")

LOGS_DIR = BASE_DIR / "logs"

DOCS_DIR = BASE_DIR / "docs"

METRICS_DIR = BASE_DIR / "metrics"

HISTORY_DIR = BASE_DIR / "history"


API_TIMEOUT = 120


DEFAULT_CONFIDENCE = "low"

DEFAULT_STATUS = "investigating"


SUPPORTED_SEVERITIES = [
    "Low",
    "Medium",
    "High"
]


OPENAI_EMBEDDING_MODEL = (
    "text-embedding-3-small"
)


SIMILARITY_TOP_K = 3