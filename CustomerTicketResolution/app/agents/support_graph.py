
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from app.services.business_service import (
    get_ticket,
    get_booking,
    get_customer,
    get_customer_tickets,
)

from app.rag.retriever import retrieve_knowledge


# Shared state passed between LangGraph nodes
class SupportState(TypedDict, total=False):
    ticket_id: str
    ticket: dict[str, Any]
    booking: dict[str, Any] | None
    customer: dict[str, Any] | None
    customer_history: list[dict[str, Any]]
    knowledge: list[dict[str, Any]]
    data_integrity_warnings: list[str]
    error: str


# Node 1: Investigate the ticket using business data
def investigate_ticket_node(state: SupportState) -> dict:

    ticket_id = state["ticket_id"]

    ticket = get_ticket(ticket_id)

    if not ticket:
        return {
            "error": f"Ticket not found: {ticket_id}"
        }

    booking = None
    if ticket.get("booking_id"):
        booking = get_booking(ticket["booking_id"])

    customer = None
    customer_history = []

    if ticket.get("customer_id"):
        customer = get_customer(ticket["customer_id"])
        customer_history = get_customer_tickets(
            ticket["customer_id"]

    
        )
        warnings = []

    if booking and ticket.get("customer_id") != booking.get("customer_id"):
        warnings.append(
            "Customer mismatch: ticket customer ID "
            f"{ticket.get('customer_id')} does not match "
            f"booking customer ID {booking.get('customer_id')}."
        )

    return {
        "ticket": ticket,
        "booking": booking,
        "customer": customer,
        "customer_history": customer_history,
        "data_integrity_warnings": warnings
    }


# Node 2: Retrieve relevant knowledge articles
def retrieve_knowledge_node(state: SupportState) -> dict:

    if state.get("error"):
        return {"knowledge": []}

    ticket = state["ticket"]

    query = ticket["description"]

    results = retrieve_knowledge(
        query=query,
        top_k=3
    )

    return {
        "knowledge": results
    }


# Build the LangGraph workflow
def build_support_graph():

    graph = StateGraph(SupportState)

    graph.add_node(
        "investigate_ticket",
        investigate_ticket_node
    )

    graph.add_node(
        "retrieve_knowledge",
        retrieve_knowledge_node
    )

    graph.add_edge(
        START,
        "investigate_ticket"
    )

    graph.add_edge(
        "investigate_ticket",
        "retrieve_knowledge"
    )

    graph.add_edge(
        "retrieve_knowledge",
        END
    )

    return graph.compile()


support_graph = build_support_graph()
