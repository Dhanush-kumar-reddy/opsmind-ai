from langchain_community.vectorstores import FAISS

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from app.rag.document_loader import (
    load_rag_documents
)

from app.rag.text_splitter import (
    split_documents
)


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_vector_store():

    documents = load_rag_documents()

    split_docs = split_documents(documents)

    vector_store = FAISS.from_documents(
        split_docs,
        embedding_model
    )

    return vector_store