from app.tools.retrieval_tool import (
    retrieval_tool
)


def retrieve_context(incident: dict):

    description = incident["description"]

    retrieved_chunks = retrieval_tool(
        description
    )

    relevant_logs = []

    relevant_docs = []

    for chunk in retrieved_chunks:

        metadata = chunk["metadata"]

        if metadata["type"] == "log":

            relevant_logs.append({
                "file": metadata["source"],
                "entries": (
                    chunk["content"].splitlines()
                )
            })

        elif metadata["type"] == "document":

            relevant_docs.append({
                "file": metadata["source"],
                "content": chunk["content"]
            })

    return {
        "incident": incident,
        "relevant_logs": relevant_logs,
        "relevant_docs": relevant_docs
    }