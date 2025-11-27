from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.config import settings
from backend.app.db.models import ChatMessage, Base
from langchain_core.messages import HumanMessage, AIMessage

engine = create_engine(settings.sqlite_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def get_chat_history(session_id: str) -> List:
    db = get_db()
    try:
        msgs = db.query(ChatMessage).filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
        return [
            HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content) for m in msgs
        ]
    finally:
        db.close()


def save_chat_message(session_id: str, message):
    db = get_db()
    try:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        db_msg = ChatMessage(
            session_id=session_id,
            role=role,
            content=message.content
        )
        db.add(db_msg)
        db.commit()
    finally:
        db.close()
