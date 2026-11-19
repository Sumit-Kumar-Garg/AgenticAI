"""LLM provider setup shared by the whole app.

Pick a provider with LLM_PROVIDER = gemini (default) | groq | openai.

- get_llm(): LangChain chat model, used by the LangGraph triage workflow.
- get_chat_client(): OpenAI-compatible client + model name, used by the tool-calling
  investigator agent and /tickets/analyze. Gemini and Groq both expose an
  OpenAI-compatible endpoint, so one code path works for all three providers.
"""
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

# provider -> (OpenAI-compatible base URL, API key env vars, model env var, default model)
_PROVIDERS = {
    "gemini": (
        "https://generativelanguage.googleapis.com/v1beta/openai/",
        ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    ),
    "groq": ("https://api.groq.com/openai/v1", ("GROQ_API_KEY",), "GROQ_MODEL", "llama-3.3-70b-versatile"),
    "openai": (None, ("OPENAI_API_KEY",), "OPENAI_MODEL", "gpt-4o-mini"),
}


def get_provider() -> str:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider not in _PROVIDERS:
        raise ValueError(f"LLM_PROVIDER must be one of {sorted(_PROVIDERS)}, got {provider!r}")
    return provider


def _api_key(env_names: tuple[str, ...]) -> str:
    for name in env_names:
        if os.getenv(name):
            return os.environ[name]
    raise RuntimeError(f"Missing API key: set {' or '.join(env_names)} in .env")


def get_google_api_key() -> str:
    """Key for Gemini embeddings (used by the ChromaDB knowledge base)."""
    return _api_key(_PROVIDERS["gemini"][1])


@lru_cache(maxsize=1)
def get_llm():
    provider = get_provider()
    _, key_names, model_env, default_model = _PROVIDERS[provider]
    model = os.getenv(model_env, default_model)
    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(model=model, temperature=0, api_key=_api_key(key_names))
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, temperature=0, api_key=_api_key(key_names))

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=model, temperature=0, google_api_key=_api_key(key_names))


@lru_cache(maxsize=1)
def get_chat_client():
    """Return (OpenAI-compatible client, model name) for the configured provider."""
    from openai import OpenAI

    base_url, key_names, model_env, default_model = _PROVIDERS[get_provider()]
    client = OpenAI(api_key=_api_key(key_names), base_url=base_url)
    return client, os.getenv(model_env, default_model)


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
