from app.loaders.log_loader import load_all_logs
from app.loaders.document_loader import load_all_documents

from app.rag.vector_store import VectorStore


vector_store = VectorStore()


def build_vector_store():

    logs = load_all_logs()
    docs = load_all_documents()

    texts = []
    metadata = []

    for log_file, entries in logs.items():

        combined_logs = "\n".join(entries)

        texts.append(combined_logs)

        metadata.append({
            "type": "log",
            "source": log_file
        })

    for doc_file, content in docs.items():

        texts.append(content)

        metadata.append({
            "type": "document",
            "source": doc_file
        })

    vector_store.add_documents(
        texts=texts,
        metadata=metadata
    )


def semantic_search(query: str):

    return vector_store.search(query)