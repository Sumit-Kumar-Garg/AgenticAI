"""Webhook for your ticketing tool. Run:  uvicorn app.api:api --reload"""
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from app.runner import run_ticket

load_dotenv()
api = FastAPI(title="Ticket triage")
REVIEW_QUEUE: list[dict] = []  # in-memory; replace with your ticketing tool's API or a DB


class TicketIn(BaseModel):
    ticket_id: str
    text: str


def _check_token(token):
    expected = os.getenv("WEBHOOK_TOKEN")
    if expected and token != expected:
        raise HTTPException(status_code=401, detail="bad token")


@api.post("/triage")
def triage(ticket: TicketIn, x_webhook_token: str | None = Header(default=None)):
    _check_token(x_webhook_token)
    result = run_ticket(ticket.ticket_id, ticket.text, mode="batch")
    if result["route"] == "human_review_queue":
        REVIEW_QUEUE.append({"ticket_id": ticket.ticket_id, **result})
    return {"ticket_id": ticket.ticket_id, **result}


@api.get("/queue")
def queue(x_webhook_token: str | None = Header(default=None)):
    _check_token(x_webhook_token)
    return REVIEW_QUEUE
