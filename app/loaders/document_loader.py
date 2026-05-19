from app.utils.file_utils import DOCS_DIR


def load_document(filename: str) -> str:
    file_path = DOCS_DIR / filename

    with open(file_path, "r") as file:
        document = file.read()

    return document


def load_all_documents() -> dict:
    documents = {}

    for file_path in DOCS_DIR.glob("*.txt"):
        with open(file_path, "r") as file:
            documents[file_path.name] = file.read()

    return documents