from typing import List, Optional
from langchain_chroma import Chroma
from langchain.storage import create_kv_docstore, LocalFileStore
from langchain_core.documents import Document
from langchain.retrievers import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.app.core.config import settings
from backend.app.core.embedding import get_embedding

_vectorstore: Optional[Chroma] = None
_parent_doc_retriever: Optional[ParentDocumentRetriever] = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=get_embedding(),
            persist_directory=str(settings.chroma_persist_directory),
        )
    return _vectorstore


def get_parent_document_retriever() -> ParentDocumentRetriever:
    global _parent_doc_retriever
    if _parent_doc_retriever is None:
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size_child,
            chunk_overlap=settings.chunk_overlap_child,
        )
        parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size_parent,
            chunk_overlap=settings.chunk_overlap_parent,
        )
        docstore_path = settings.root_dir / "docstore"
        docstore = create_kv_docstore(LocalFileStore(str(docstore_path)))
        _parent_doc_retriever = ParentDocumentRetriever(
            vectorstore=get_vectorstore(),
            docstore=docstore,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter,
        )
    return _parent_doc_retriever


def add_documents_to_vectorstore(documents: List[Document]) -> None:
    retriever = get_parent_document_retriever()
    retriever.add_documents(documents)


def similarity_search(query: str, k: int = 4) -> List[Document]:
    retriever = get_parent_document_retriever()
    return retriever.invoke(query, k=k)
