from backend.app.core.llm import get_llm
from backend.app.agents.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage


def rewrite_query_node(state: AgentState) -> dict:
    original_query = state["original_query"]
    messages = state["messages"]
    if not original_query.strip():
        return {"rewritten_query": ""}
    history = ""
    for msg in messages[-10:]:
        if isinstance(msg, HumanMessage):
            history += f"用户：{msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"客服：{msg.content}\n"
    prompt = f"""
你是一个企业知识库检索助手，请严格按以下规则操作：
- 参考对话历史
- 仅输出改写后的问题，不要任何解释、说明、括号或额外内容。
- 保留用户原始意图。
- 补充缺失的上下文。
- 使用正式、简洁、完整的中文问句。
对话历史：{history}
当前问题：{original_query}
改写后问题：
""".strip()
    llm = get_llm(temperature=0.0)
    rewritten = llm.invoke(prompt).content
    return {"rewritten_query": rewritten}
