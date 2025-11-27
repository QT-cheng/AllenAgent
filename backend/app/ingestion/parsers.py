from pathlib import Path
from typing import Union, List
from unstructured.partition.auto import partition
from unstructured.documents.elements import Element
from backend.app.core.config import settings


def parse_document(file_path: Union[str, Path]) -> str:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    try:
        elements: List[Element] = partition(
            filename=str(file_path),
            strategy=settings.partition_strategy,
            include_page_breaks=False,
        )
    except Exception as e:
        raise RuntimeError(f"文档解析失败 ({file_path}): {e}")
    texts = []
    for elem in elements:
        if hasattr(elem, "text") and elem.text.strip():
            texts.append(elem.text.strip())
    return "\n".join(texts)
