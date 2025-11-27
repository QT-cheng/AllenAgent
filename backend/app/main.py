from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.chat import router as chat_router
from backend.app.api.documents import router as documents_router
from backend.app.db.session import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Allen Agent - 企业智能客服",
    description="基于LangGraph的RAG智能回答系统",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router)
app.include_router(documents_router)
