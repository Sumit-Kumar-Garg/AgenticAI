# AgenticAI

Hands-on projects building **LLM agents** that do real work, with guardrails, human-in-the-loop review and evaluation.

## Projects

| Project | What it does | Stack |
|---|---|---|
| [CustomerTicketResolution](CustomerTicketResolution/) | Triage agent that classifies, prioritises and routes support tickets. It masks PII, retrieves similar resolved tickets, applies guardrails and sends risky cases to a human. Benchmarked against a classical ML baseline. | LangGraph, Gemini, FastAPI, ChromaDB, scikit-learn, Pydantic |
