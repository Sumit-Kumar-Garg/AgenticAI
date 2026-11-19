from functools import lru_cache

from app.llm import get_google_api_key

EMBEDDING_MODEL = "gemini-embedding-001"


@lru_cache(maxsize=1)
def _client():
    from google import genai

    return genai.Client(api_key=get_google_api_key())


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = _client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]
