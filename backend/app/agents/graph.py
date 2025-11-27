from langgraph.graph import StateGraph, END
from backend.app.agents.state import AgentState
from backend.app.agents.nodes.rewrite import rewrite_query_node
from backend.app.agents.nodes.retrieve import retrieve_docs_node
from backend.app.agents.nodes.generate import generate_answer_node
from backend.app.agents.nodes.selfcheck import self_check_node

def create_agent_graph() -> StateGraph:
    workflow = StateGraph(AgentState)
    workflow.add_node("rewrite", rewrite_query_node)
    workflow.add_node("retrieve", retrieve_docs_node)
    workflow.add_node("generate", generate_answer_node)
    workflow.add_node("self_check", self_check_node)
    workflow.set_entry_point("rewrite")
    workflow.add_edge("rewrite", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "self_check")
    def should_retry(state: AgentState) -> str:
        if state["needs_correction"]:
            return "rewrite"
        else:
            return END
    workflow.add_conditional_edges(
        "self_check",
        should_retry,
        {
            "rewrite": "rewrite",
            END: END,
        }
    )
    return workflow
app_agent = create_agent_graph().compile()