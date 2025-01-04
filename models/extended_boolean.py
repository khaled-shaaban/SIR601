import math

class ExtendedBooleanModel:
    def __init__(self, documents):
        """
        Initialize the Extended Boolean Model.
        :param documents: List of documents where each document is a dictionary with 'id' and 'text'.
        """
        self.documents = documents
        self.inverted_index = self._build_inverted_index()

    def _build_inverted_index(self):
        """
        Build an inverted index with term frequency.
        :return: Dictionary with terms as keys and (document ID, frequency) pairs as values.
        """
        inverted_index = {}
        for doc in self.documents:
            doc_id = doc['id']
            tokens = doc['text'].lower().split()
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = {}
                inverted_index[token][doc_id] = inverted_index[token].get(doc_id, 0) + 1
        return inverted_index

    def search(self, query, alpha=0.5):
        """
        Perform an extended Boolean search with weights.
        :param query: List of terms and their weights, e.g., [("term1", 0.8), ("term2", 0.2)].
        :param alpha: Weighting parameter (default 0.5).
        :return: Dictionary of document IDs and relevance scores.
        """
        scores = {doc['id']: 0 for doc in self.documents}
        for term, weight in query:
            if term in self.inverted_index:
                for doc_id, freq in self.inverted_index[term].items():
                    scores[doc_id] += weight * freq

        # Normalize scores
        max_score = max(scores.values())
        if max_score > 0:
            scores = {doc_id: (score / max_score) ** alpha for doc_id, score in scores.items()}
        return scores
