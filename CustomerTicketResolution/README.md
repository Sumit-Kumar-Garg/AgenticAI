# Support ticket triage agent (LangGraph, free tier)

Flow: mask PII -> retrieve similar resolved tickets -> LLM classify -> decide -> auto-assign or human review.

## Setup (Intel Mac, no Homebrew or Ollama needed)
    python3.12 -m venv .venv && source .venv/bin/activate
    pip install --upgrade pip && pip install -r requirements.txt
    cp .env.example .env     # then add GOOGLE_API_KEY (or GROQ_API_KEY and LLM_PROVIDER=groq)

## Run
    python main.py                       # interactive demo, pauses for a human on risky tickets
    python -m evals.run_eval             # accuracy vs data/golden_tickets.csv
    uvicorn app.api:api --reload         # webhook: POST /triage, GET /queue
    jupyter lab                          # open triage_baseline_vs_llm.ipynb (baseline vs agent comparison)

## Make it yours
1. Edit app/config.py: TEAMS, thresholds, escalation keywords.
2. Replace data/resolved_tickets.csv (knowledge base) and data/golden_tickets.csv (eval set) with real, anonymized tickets. Keep the two sets separate.
3. Run the eval, tune the prompt in app/graph.py, rerun. Run in shadow mode before enabling auto-assign.

## Notes
- Check current free-tier model names in Google AI Studio / Groq docs and set GEMINI_MODEL / GROQ_MODEL in .env.
- Free tiers have rate limits; raise EVAL_DELAY if you hit them.
- Free-tier providers may use your data; mask PII and avoid sensitive tickets until you've reviewed their terms.
- Optional tracing: add Langfuse keys to .env.
