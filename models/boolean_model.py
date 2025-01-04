class BooleanModel:
    def __init__(self, documents):
        """
        Initialize the Boolean Model.
        :param documents: List of documents where each document is a dictionary with 'id' and 'text'.
        """
        self.documents = documents
        self.inverted_index = self._build_inverted_index()

    def _build_inverted_index(self):
        """
        Build an inverted index from the documents.
        :return: Dictionary with terms as keys and document IDs as values.
        """
        inverted_index = {}
        for doc in self.documents:
            doc_id = doc['id']
            tokens = doc['text'].lower().split()  # Simple tokenization
            for token in tokens:
                if token not in inverted_index:
                    inverted_index[token] = set()
                inverted_index[token].add(doc_id)
        return inverted_index

    def search(self, query):
        """
        Perform a Boolean search using AND, OR, and NOT operators.
        :param query: Query string in the form "term1 AND term2" or "term1 OR term2".
        :return: Set of document IDs matching the query.
        """
        query = query.lower()
        terms = query.split()
        result_set = set()

        if "and" in terms:
            term1, _, term2 = terms
            result_set = self.inverted_index.get(term1, set()) & self.inverted_index.get(term2, set())
        elif "or" in terms:
            term1, _, term2 = terms
            result_set = self.inverted_index.get(term1, set()) | self.inverted_index.get(term2, set())
        elif "not" in terms:
            _, term = terms
            all_docs = set(doc['id'] for doc in self.documents)
            result_set = all_docs - self.inverted_index.get(term, set())
        else:
            result_set = self.inverted_index.get(terms[0], set())

        return result_set
