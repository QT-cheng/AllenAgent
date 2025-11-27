from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document

from backend.app.ingestion.parsers import parse_document
from backend.app.db.vector_store import add_documents_to_vectorstore, get_parent_document_retriever, get_vectorstore


def load_document(file_path: Union[str, Path]) -> List[str]:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    text = parse_document(file_path)
    if not text.strip():
        raise ValueError("文档无有效文本内容")
    doc = Document(
        page_content=text,
        metadata={"source": str(file_path.resolve()), "filename": file_path.name}
    )
    add_documents_to_vectorstore([doc])
    return [str(file_path.name)]
