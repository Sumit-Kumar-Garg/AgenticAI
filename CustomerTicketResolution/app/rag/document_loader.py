
import json
from pathlib import Path


KNOWLEDGE_BASE_PATH = Path("data/knowledge_base.json")


def load_knowledge_articles():
    if not KNOWLEDGE_BASE_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_BASE_PATH}"
        )

    with KNOWLEDGE_BASE_PATH.open("r", encoding="utf-8") as file:
        articles = json.load(file)

    if not isinstance(articles, list):
        raise ValueError("Knowledge base must contain a list of articles")

    documents = []

    for article in articles:
        required_fields = ["article_id", "issue", "solution"]

        for field in required_fields:
            if not article.get(field):
                raise ValueError(
                    f"Article is missing required field: {field}"
                )

        documents.append({
            "id": article["article_id"],
            "text": (
                f"Issue: {article['issue']}\n"
                f"Solution: {article['solution']}"
            ),
            "metadata": {
                "article_id": article["article_id"],
                "issue": article["issue"]
            }
        })

    return documents
