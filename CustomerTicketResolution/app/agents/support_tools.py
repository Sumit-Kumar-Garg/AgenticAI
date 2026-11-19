from app.rag.retriever import retrieve_knowledge

from app.services.business_service import (
    get_customer,
    get_booking,
    get_ticket,
    get_customer_tickets
)
from app.rag.retriever import retrieve_knowledge


def search_support_knowledge(query: str, top_k: int = 3):
    """Search support knowledge articles using semantic similarity."""
    return retrieve_knowledge(query=query, top_k=top_k)




def lookup_ticket(ticket_id: str):
    """
    Retrieve support ticket information.
    """
    return get_ticket(ticket_id)


def lookup_booking(booking_id: str):
    """
    Retrieve booking and hotel information.
    """
    return get_booking(booking_id)


def lookup_customer(customer_id: str):
    """
    Retrieve customer information.
    """
    return get_customer(customer_id)


def lookup_customer_history(customer_id: str):
    """
    Retrieve customer's historical tickets.
    """
    return get_customer_tickets(customer_id)
