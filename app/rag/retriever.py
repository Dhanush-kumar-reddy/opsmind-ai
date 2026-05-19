from app.rag.vector_store import (
    build_vector_store
)


vector_store = build_vector_store()

retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)


def retrieve_documents(query: str):

    results = retriever.invoke(query)

    return results