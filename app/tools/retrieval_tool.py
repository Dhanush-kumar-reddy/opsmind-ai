from app.rag.retriever import (
    retrieve_documents
)


def retrieval_tool(query: str):

    results = retrieve_documents(query)

    formatted_results = []

    for result in results:

        formatted_results.append({
            "content": result.page_content,
            "metadata": result.metadata
        })

    return formatted_results