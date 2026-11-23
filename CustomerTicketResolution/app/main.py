from fastapi import FastAPI, HTTPException
from app.models.ticket import InvestigationRequest

from app.agents.support_agent import investigate_ticket

from app.models.ticket import TicketRequest
from app.services.ai_service import analyze_ticket

from app.models.ticket import (
    InvestigationRequest,
    InvestigationResponse
)

from app.agents.support_graph import support_graph

from uuid import uuid4

from langgraph.types import Command

from app.models.ticket import (
    InvestigationRequest,
    HumanReviewDecision
)
from app.services.audit_service import (
    initialize_audit_table,
    save_human_review,
    get_review_audit
)

initialize_audit_table()

app = FastAPI(
    title="Agentic AI Support Platform",
    description="AI-powered customer support ticket analysis",
    version="1.0.0"
)

@app.get("/tickets/{ticket_id}/audit")
def get_ticket_audit(ticket_id: str):

    records = get_review_audit(ticket_id)

    return {
        "ticket_id": ticket_id,
        "total_reviews": len(records),
        "audit_records": records
    }

@app.post("/tickets/investigate")
def investigate_ticket_api(request: InvestigationRequest):

    # Every investigation gets a unique workflow thread.
    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        result = support_graph.invoke(
            {"ticket_id": request.ticket_id},
            config=config
        )

        if result.get("error"):
            raise HTTPException(
                status_code=404,
                detail=result["error"]
            )

        interrupts = result.get("__interrupt__", [])

        if not interrupts:
            return {
            "status": result.get("final_status", "COMPLETED"),
            "ticket_id": request.ticket_id,
            "thread_id": thread_id,
            "analysis": result.get("analysis"),
            "recommendation": (
                result.get("analysis", {}).get("recommended_action")
            ),
            "data_integrity_warnings": result.get(
                "data_integrity_warnings", []
            )
        }

        return {
            "status": "PENDING_HUMAN_REVIEW",
            "ticket_id": request.ticket_id,
            "thread_id": thread_id,
            "review_request": interrupts[0].value
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/tickets/review/{thread_id}")
def submit_human_review(
    thread_id: str,
    request: HumanReviewDecision
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    decision = {
        "approved": request.approved,
        "reviewer": request.reviewer,
        "comment": request.comment
    }

    try:
        result = support_graph.invoke(
            Command(resume=decision),
            config=config
        )

        final_status = result.get("final_status")

        if final_status not in ["APPROVED", "REJECTED"]:
            raise HTTPException(
                status_code=409,
                detail="Workflow did not complete the human review."
            )

        # Persist the review decision.
        save_human_review(
            ticket_id=result["ticket_id"],
            thread_id=thread_id,
            reviewer=request.reviewer,
            approved=request.approved,
            comment=request.comment,
            final_status=final_status
        )

        return {
            "status": final_status,
            "thread_id": thread_id,
            "ticket_id": result.get("ticket_id"),
            "human_decision": result.get("human_decision"),
            "analysis": result.get("analysis")
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/tickets/{ticket_id}/audit")
def get_ticket_audit(ticket_id: str):

    records = get_review_audit(ticket_id)

    return {
        "ticket_id": ticket_id,
        "total_reviews": len(records),
        "audit_records": records
    }

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