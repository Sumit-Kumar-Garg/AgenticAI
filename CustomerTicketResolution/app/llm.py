"""Gemini setup shared by the whole app. Settings come from .env:

    OPENAI_API_KEY=<your Gemini API key>
    OPENAI_MODEL=<Gemini model name>

- get_llm(): LangChain Gemini chat model (LangGraph triage workflow).
- get_chat_client(): Gemini through its OpenAI-compatible endpoint, used by the
  tool-calling investigator agent and /tickets/analyze.
- get_api_key(): the same key, used for Gemini embeddings.
"""
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

GEMINI_OPENAI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-2.5-flash"


def get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Missing Gemini API key: set OPENAI_API_KEY in .env")
    return key


def get_model() -> str:
    return os.getenv("OPENAI_MODEL") or DEFAULT_MODEL


@lru_cache(maxsize=1)
def get_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=get_model(), temperature=0, google_api_key=get_api_key())


@lru_cache(maxsize=1)
def get_chat_client():
    """Return (client, model name) for Gemini's OpenAI-compatible API."""
    from openai import OpenAI

    return OpenAI(api_key=get_api_key(), base_url=GEMINI_OPENAI_URL), get_model()


def get_callbacks():
    """Langfuse tracing, only if keys are set. Handles both SDK import paths."""
    if not (os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")):
        return []
    try:
        from langfuse.langchain import CallbackHandler  # langfuse v3
    except ImportError:
        try:
            from langfuse.callback import CallbackHandler  # langfuse v2
        except ImportError:
            return []
    try:
        return [CallbackHandler()]
    except Exception:
        return []
