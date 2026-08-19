"""
ai_assistant.py
A lightweight, retrieval-based product Q&A assistant.
Uses TF-IDF + cosine similarity to match customer questions
against product descriptions - no external API required.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductAssistant:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.product_vectors = None
        self.products = []

    def fit(self, products):
        """
        products: list of dicts, each with at least 'name', 'description', 'category'.
        Builds the TF-IDF matrix from product text (name + brand + category + description).
        Safely does nothing if there are no products yet (e.g. fresh database).
        """
        self.products = products

        if not products:
            self.product_vectors = None
            return

        corpus = [
            f"{p['name']} {p['brand']} {p['category']} {p['description']}"
            for p in products
        ]
        self.product_vectors = self.vectorizer.fit_transform(corpus)

    def ask(self, question, top_k=3):
        """
        Returns the top_k most relevant products for a given question,
        along with a similarity score (0 to 1).
        """
        if self.product_vectors is None or len(self.products) == 0:
            return []

        question_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(question_vector, self.product_vectors)[0]

        ranked = sorted(
            zip(self.products, scores), key=lambda x: x[1], reverse=True
        )

        results = []
        for product, score in ranked[:top_k]:
            if score > 0:
                results.append({**product, "match_score": round(float(score), 3)})

        return results
