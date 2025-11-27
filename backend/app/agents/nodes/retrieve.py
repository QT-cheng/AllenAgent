from backend.app.agents.state import AgentState
from backend.app.db.vector_store import similarity_search


def retrieve_docs_node(state: AgentState) -> dict:
    rewritten_query = state["rewritten_query"].strip()
    if not rewritten_query:
        return {"retrieved_docs": []}
    docs = similarity_search(rewritten_query, k=4)
    return {"retrieved_docs": docs}
