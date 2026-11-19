
import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("OPENAI_API_KEY"))



EMBEDDING_MODEL = "gemini-embedding-001"


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]

