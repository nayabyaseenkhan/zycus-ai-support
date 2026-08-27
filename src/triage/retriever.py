from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils.kb_loader import load_knowledge_base_chunks


class KnowledgeBaseRetriever:
    """Retrieve relevant knowledge-base chunks using TF-IDF similarity."""

    def __init__(self):
        self.chunks = load_knowledge_base_chunks()

        if not self.chunks:
            raise ValueError("Knowledge base contains no chunks.")

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
        )

        self.chunk_vectors = self.vectorizer.fit_transform(
            [chunk["content"] for chunk in self.chunks]
        )

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Return the most relevant knowledge-base chunks."""

        if not query.strip():
            return []

        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.chunk_vectors,
        )[0]

        ranked_indices = similarities.argsort()[::-1][:top_k]

        results = []

        for index in ranked_indices:
            chunk = self.chunks[index].copy()
            chunk["score"] = float(similarities[index])
            results.append(chunk)

        return results