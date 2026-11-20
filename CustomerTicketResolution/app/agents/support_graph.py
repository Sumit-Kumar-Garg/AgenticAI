
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from app.services.business_service import (
    get_ticket,
    get_booking,
    get_customer,
    get_customer_tickets,
)

from app.rag.retriever import retrieve_knowledge

from app.services.reasoning_service import analyze_support_case


# Shared state between all LangGraph nodes
class SupportState(TypedDict, total=False):
    ticket_id: str
    ticket: dict[str, Any]
    booking: dict[str, Any] | None
    customer: dict[str, Any] | None
    customer_history: list[dict[str, Any]]
    data_integrity_warnings: list[str]
    knowledge: list[dict[str, Any]]
    analysis: dict[str, Any]
    error: str


# NODE 1: Investigate ticket and business data
def investigate_ticket_node(state: SupportState) -> dict:

    ticket_id = state["ticket_id"]

    ticket = get_ticket(ticket_id)

    if not ticket:
        return {
            "error": f"Ticket not found: {ticket_id}"
        }

    booking = None
    customer = None
    customer_history = []
    warnings = []

    if ticket.get("booking_id"):
        booking = get_booking(ticket["booking_id"])

    if ticket.get("customer_id"):
        customer = get_customer(ticket["customer_id"])

        customer_history = get_customer_tickets(
            ticket["customer_id"]
        )

    # Validate ticket-booking relationship
    if booking and (
        ticket.get("customer_id") != booking.get("customer_id")
    ):
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


# CONDITIONAL ROUTING: Stop if ticket was not found
def route_after_investigation(state: SupportState):

    if state.get("error"):
        return "stop"

    return "continue"


# NODE 2: Retrieve relevant knowledge
def retrieve_knowledge_node(state: SupportState) -> dict:

    ticket = state["ticket"]

    results = retrieve_knowledge(
        query=ticket["description"],
        top_k=3
    )

    return {
        "knowledge": results
    }


# NODE 3: Gemini reasoning
def gemini_reasoning_node(state: SupportState) -> dict:

    case_context = {
        "ticket": state["ticket"],
        "booking": state.get("booking"),
        "customer": state.get("customer"),
        "customer_history": state.get("customer_history", []),
        "data_integrity_warnings": state.get(
            "data_integrity_warnings", []
        ),
        "knowledge": state.get("knowledge", [])
    }

    analysis = analyze_support_case(case_context)

    # Deterministic safety check:
    # Never allow Gemini to dismiss an existing data-integrity warning.
    warnings = state.get("data_integrity_warnings", [])

    if warnings:
        analysis["requires_human"] = True

    return {
        "analysis": analysis
    }


# BUILD THE GRAPH
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

    graph.add_node(
        "gemini_reasoning",
        gemini_reasoning_node
    )

    graph.add_edge(
        START,
        "investigate_ticket"
    )

    graph.add_conditional_edges(
        "investigate_ticket",
        route_after_investigation,
        {
            "continue": "retrieve_knowledge",
            "stop": END
        }
    )

    graph.add_edge(
        "retrieve_knowledge",
        "gemini_reasoning"
    )

    graph.add_edge(
        "gemini_reasoning",
        END
    )

    return graph.compile()


support_graph = build_support_graph()
