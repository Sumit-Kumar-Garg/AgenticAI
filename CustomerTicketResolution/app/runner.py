import uuid

from langgraph.types import Command

from app.graph import build_graph
from app.llm import get_callbacks

_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def run_ticket(ticket_id: str, text: str, mode: str = "batch", ask_human=None) -> dict:
    """Run one ticket through the graph.

    mode="batch": never pauses; risky tickets are routed to 'human_review_queue'.
    mode="interactive": pauses at human review; ask_human(payload) must return overrides dict.
    """
    graph = get_graph()
    config = {
        "configurable": {"thread_id": f"{ticket_id}-{uuid.uuid4().hex[:8]}"},
        "callbacks": get_callbacks(),
    }
    result = graph.invoke({"ticket_id": ticket_id, "raw_text": text, "mode": mode}, config)

    if "__interrupt__" in result and ask_human is not None:
        payload = result["__interrupt__"][0].value
        overrides = ask_human(payload)
        result = graph.invoke(Command(resume=overrides), config)

    return result["final"]
