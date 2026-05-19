from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


def split_documents(documents):

    split_docs = text_splitter.split_documents(
        documents
    )

    return split_docs