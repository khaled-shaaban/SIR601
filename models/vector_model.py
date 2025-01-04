import math
from collections import Counter

class VectorModel:
    def __init__(self, documents):
        """
        Initialize the Vector Space Model.
        :param documents: List of documents where each document is a dictionary with 'id' and 'text'.
        """
        self.documents = documents
        self.doc_vectors = self._build_document_vectors()
        self.doc_magnitudes = self._calculate_magnitudes()

    def _build_document_vectors(self):
        """
        Convert documents into term frequency vectors.
        :return: Dictionary of document IDs and term frequency vectors.
        """
        vectors = {}
        for doc in self.documents:
            doc_id = doc['id']
            tokens = doc['text'].lower().split()
            vectors[doc_id] = Counter(tokens)
        return vectors

    def _calculate_magnitudes(self):
        """
        Calculate the magnitude of each document vector.
        :return: Dictionary of document IDs and magnitudes.
        """
        magnitudes = {}
        for doc_id, vector in self.doc_vectors.items():
            magnitudes[doc_id] = math.sqrt(sum(freq ** 2 for freq in vector.values()))
        return magnitudes

    def search(self, query):
        """
        Perform a cosine similarity search.
        :param query: Query string.
        :return: Dictionary of document IDs and similarity scores.
        """
        query_vector = Counter(query.lower().split())
        query_magnitude = math.sqrt(sum(freq ** 2 for freq in query_vector.values()))
        scores = {}

        for doc_id, doc_vector in self.doc_vectors.items():
            dot_product = sum(query_vector[term] * doc_vector.get(term, 0) for term in query_vector)
            if query_magnitude * self.doc_magnitudes[doc_id] > 0:
                scores[doc_id] = dot_product / (query_magnitude * self.doc_magnitudes[doc_id])
            else:
                scores[doc_id] = 0.0

        return scores
