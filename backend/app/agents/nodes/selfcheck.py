from backend.app.core.llm import get_llm
from backend.app.agents.state import AgentState


def self_check_node(state: AgentState) -> dict:
    draft_answer = state["draft_answer"]
    docs = state["retrieved_docs"]
    count_generate = state.get("count_generate", 0)
    if count_generate >= 3:
        return {
            "final_answer": "抱歉，经过多次尝试仍无法找到可靠答案。可能是知识库中缺少相关信息或问题表述不清晰。",
            "needs_correction": False
        }
    if not docs:
        return {
            "final_answer": draft_answer,
            "needs_correction": False
        }
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""
你是一个事实核查员，请严格判断以下回答是否完全基于提供的参考资料。
- 如果回答中的所有信息都能在参考资料中找到依据，请回答 "yes"。
- 如果回答包含参考资料中没有的信息、推测、常识或外部知识，请回答 "no"。
- 仅输出 "yes" 或 "no"，不要任何解释。
参考资料：
{context}
回答：
{draft_answer}
是否基于资料？
""".strip()
    llm = get_llm(temperature=0.0)  # 确定性判断
    response = llm.invoke(prompt).content.strip()
    needs_correction = "no" in response
    if needs_correction:
        return {
            "final_answer": "检测到回答可能存在不准确信息，正在重新生成……",
            "needs_correction": True,
            "count_generate": count_generate + 1
        }
    else:
        return {
            "final_answer": draft_answer,
            "needs_correction": False
        }
