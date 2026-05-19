from langchain_community.vectorstores import FAISS

from langchain_openai import (
    OpenAIEmbeddings
)

from app.utils.config import (
    OPENAI_API_KEY
)

from app.rag.document_loader import (
    load_rag_documents
)

from app.rag.text_splitter import (
    split_documents
)


embedding_model = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY,
    model="text-embedding-3-small"
)


def build_vector_store():

    documents = load_rag_documents()

    split_docs = split_documents(
        documents
    )

    vector_store = FAISS.from_documents(
        split_docs,
        embedding_model
    )

    vector_store.save_local(
        "faiss_index"
    )

    return vector_store


def load_vector_store():

    vector_store = FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return vector_store


if __name__ == "__main__":

    print("Building vector store...")

    build_vector_store()

    print("Vector store created.")