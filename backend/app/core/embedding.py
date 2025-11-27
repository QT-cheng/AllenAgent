from typing import List
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from backend.app.core.config import settings


class Embedding(Embeddings):

    def __init__(self):
        self.model = SentenceTransformer(
            settings.embedding_model,
            cache_folder=str(settings.root_dir / "models"),
            trust_remote_code=True
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = [text.replace("\n", " ") for text in texts if text.strip()]
        if not texts:
            return []
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


_embedding_instance: Embedding = None


def get_embedding() -> Embedding:
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = Embedding()
    return _embedding_instance
