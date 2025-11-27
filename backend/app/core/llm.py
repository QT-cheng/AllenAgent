from langchain_openai import ChatOpenAI
from backend.app.core.config import settings


def get_llm(temperature: float = settings.temperature, max_tokens: int | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.deepseek_api_key,
        base_url="https://api.deepseek.com",
        temperature=temperature,
        max_tokens=max_tokens,
        model_kwargs={"stream": False},
    )
