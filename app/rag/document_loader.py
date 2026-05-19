from langchain_core.documents import Document

from app.loaders.log_loader import load_all_logs
from app.loaders.document_loader import load_all_documents


def load_rag_documents():

    documents = []

    logs = load_all_logs()

    docs = load_all_documents()

    for log_file, log_entries in logs.items():

        content = "\n".join(log_entries)

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "type": "log",
                    "source": log_file
                }
            )
        )

    for doc_file, content in docs.items():

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "type": "document",
                    "source": doc_file
                }
            )
        )

    return documents