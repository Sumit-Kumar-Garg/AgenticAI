from pydantic import BaseModel, Field
from typing import Literal


class TicketRequest(BaseModel):
    ticket_id: str
    description: str

class InvestigationRequest(BaseModel):
    ticket_id: str
    
class TicketAnalysis(BaseModel):

    category: Literal[
        "BOOKING_CONFIRMATION",
        "PAYMENT",
        "CANCELLATION",
        "REFUND",
        "TECHNICAL",
        "OTHER"
    ]

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]

    confidence: float = Field(
        ge=0,
        le=1
    )

    recommended_action: str

    requires_human: bool