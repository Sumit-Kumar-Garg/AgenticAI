from fastapi import FastAPI, HTTPException
from app.models.ticket import InvestigationRequest

from app.agents.support_agent import investigate_ticket

from app.models.ticket import TicketRequest
from app.services.ai_service import analyze_ticket

app = FastAPI(
    title="Agentic AI Support Platform",
    description="AI-powered customer support ticket analysis",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "application": "AI Support Platform"
    }

    


@app.post("/tickets/analyze")
def analyze_support_ticket(ticket: TicketRequest):

    try:
        result = analyze_ticket(ticket.description)

        return {
            "ticket_id": ticket.ticket_id,
            "analysis": result.model_dump()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ticket analysis failed: {str(e)}"
        )


@app.post("/tickets/investigate")
def investigate_support_ticket(
    request: InvestigationRequest
):

    try:
        result = investigate_ticket(request.ticket_id)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {str(e)}"
        )