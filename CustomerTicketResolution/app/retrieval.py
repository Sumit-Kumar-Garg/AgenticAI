"""Similar-ticket lookup using TF-IDF.

Deliberately avoids embeddings/torch so it installs cleanly on an Intel Mac and costs nothing.
Swap in an embedding model later if evals show retrieval is the bottleneck.
"""
import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarTickets:
    def __init__(self, csv_path: str):
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path).fillna("")
        else:
            self.df = pd.DataFrame(columns=["ticket_id", "text", "category", "team"])
        self.vec = None
        self.matrix = None
        if len(self.df):
            self.vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.matrix = self.vec.fit_transform(self.df["text"])

    def search(self, text: str, k: int = 3, min_score: float = 0.15) -> list[dict]:
        if self.vec is None:
            return []
        sims = cosine_similarity(self.vec.transform([text]), self.matrix)[0]
        top = sims.argsort()[::-1][:k]
        out = []
        for i in top:
            if sims[i] >= min_score:
                row = self.df.iloc[i]
                out.append(
                    {
                        "ticket_id": str(row["ticket_id"]),
                        "text": row["text"],
                        "category": row["category"],
                        "team": row["team"],
                        "score": round(float(sims[i]), 2),
                    }
                )
        return out
