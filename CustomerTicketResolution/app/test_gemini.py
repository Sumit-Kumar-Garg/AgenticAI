
from app.rag.embedding_service import generate_embeddings

texts = [
    "Hotel booking confirmation issue",
    "Customer cannot find hotel reservation"
]

vectors = generate_embeddings(texts)

print("Gemini API connection successful")
print("Number of embeddings:", len(vectors))
print("Vector dimensions:", len(vectors[0]))
