from backend.app.core.llm import get_llm
from backend.app.agents.state import AgentState


def generate_answer_node(state: AgentState) -> dict:
    if state.get("count_generate", 0) >= 3:
        return {"draft_answer": "终止生成：重试次数超限"}
    original_query = state["original_query"]
    docs = state["retrieved_docs"]
    if not docs:
        return {"draft_answer": "抱歉，未在知识库中找到相关信息。"}
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""
你是一个企业智能客服，请严格根据以下参考资料回答用户问题。
- 仅使用参考资料中的信息，不说“根据资料”等冗余表述
- 如果资料无法回答问题，请说“未找到相关信息”
- 回答简洁、准确、使用正式中文
- 严格参考参考资料中的内容，不能凭空臆造
参考资料：
{context}
问题：{original_query}
回答：
""".strip()
    llm = get_llm(temperature=0.3)
    draft_answer = llm.invoke(prompt).content
    return {"draft_answer": draft_answer}
