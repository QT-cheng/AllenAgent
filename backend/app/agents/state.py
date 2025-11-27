from typing import List, TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document


class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    original_query: str
    rewritten_query: str
    retrieved_docs: List[Document]
    draft_answer: str
    final_answer: str
    needs_correction: bool
    count_generate: int
