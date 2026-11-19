from typing import Literal, Optional
from pydantic import BaseModel, Field


class Triage(BaseModel):
    """The triage contract: what the agent outputs for every ticket."""

    category: Literal["billing", "bug", "access", "how_to", "feature_request", "other"]
    priority: Literal["P1", "P2", "P3", "P4"] = Field(
        description="P1 = outage/security/money lost, P2 = broken core feature, "
        "P3 = degraded or workaround exists, P4 = question or minor request"
    )
    team: str = Field(description="One of the allowed team names, exactly as given")
    sentiment: Literal["calm", "frustrated", "angry"]
    is_duplicate_of: Optional[str] = Field(
        default=None,
        description="ticket_id of a similar ticket if this is clearly the same issue, else null",
    )
    confidence: float = Field(ge=0.0, le=1.0, description="Your confidence in category, priority and team")
    reason: str = Field(description="One sentence explaining the routing decision")
