from pydantic import BaseModel, Field
from typing import Literal


from typing import Any


class InvestigationRequest(BaseModel):
    ticket_id: str


class InvestigationResponse(BaseModel):
    ticket_id: str
    ticket: dict[str, Any] | None = None
    booking: dict[str, Any] | None = None
    customer: dict[str, Any] | None = None
    customer_history: list[dict[str, Any]] = Field(default_factory=list)
    data_integrity_warnings: list[str] = Field(default_factory=list)
    knowledge: list[dict[str, Any]] = Field(default_factory=list)
    analysis: dict[str, Any] | None = None
    error: str | None = None

class HumanReviewDecision(BaseModel):
    approved: bool
    reviewer: str = "support-agent"
    comment: str = ""
    
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