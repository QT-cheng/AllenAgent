from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = ROOT_DIR / "uploads"
CHROMA_PERSIST_DIR = ROOT_DIR / "chroma_db"
SQLITE_DB_PATH = ROOT_DIR / "data" / "app.db"


class Settings(BaseSettings):
    app_name: str = "Allen Agent"
    debug: bool = Field(default=False)
    deepseek_api_key: str
    llm_model: str
    embedding_model: str
    chroma_collection_name: str
    partition_strategy: str
    temperature: float
    chroma_persist_directory: Path = CHROMA_PERSIST_DIR
    sqlite_db_path: Path = SQLITE_DB_PATH

    @property
    def sqlite_url(self) -> str:
        return f"sqlite:///{self.sqlite_db_path.as_posix()}"

    @property
    def root_dir(self) -> Path:
        return ROOT_DIR

    chunk_size_child: int = 400
    chunk_overlap_child: int = 50
    chunk_size_parent: int = 2000
    chunk_overlap_parent: int = 200
    upload_dir: Path = UPLOAD_DIR

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
        case_sensitive=False,
    )


settings = Settings()
