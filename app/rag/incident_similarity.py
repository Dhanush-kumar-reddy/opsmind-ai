from langchain_core.documents import (
    Document
)

from app.database.incident_memory import (
    get_all_incidents
)

from app.rag.vector_store import (
    embedding_model
)

from langchain_community.vectorstores import (
    FAISS
)


def find_similar_incidents(query):

    incidents = get_all_incidents()

    documents = []

    for incident in incidents:

        content = (
            f"Service: {incident.service}\n"
            f"Severity: {incident.severity}\n"
            f"Description: "
            f"{incident.description}\n"
            f"Root Cause: "
            f"{incident.root_cause}"
        )

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "incident_id": (
                        incident.incident_id
                    ),
                    "service": (
                        incident.service
                    ),
                    "root_cause": (
                        incident.root_cause
                    )
                }
            )
        )

    if len(documents) == 0:

        return []

    vector_store = FAISS.from_documents(
        documents,
        embedding_model
    )

    results = (
        vector_store.similarity_search(
            query,
            k=3
        )
    )

    return results