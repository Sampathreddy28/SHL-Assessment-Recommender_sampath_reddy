import json
import pickle

import faiss
import numpy as np

from app.retrieval.embedder import Embedder


class VectorStore:

    def __init__(self):

        self.embedder = Embedder()

        self.index = None

        self.documents = []

    def build_documents(self, catalog):

        docs = []

        for item in catalog:

            text = f"""
            Name: {item.get('name', '')}

            Description:
            {item.get('description', '')}

            Skills:
            {', '.join(item.get('skills', []))}

            Test Type:
            {item.get('test_type', '')}
            """

            docs.append(text)

        return docs

    def create_index(self, catalog):

        self.documents = catalog

        docs = self.build_documents(catalog)

        embeddings = self.embedder.embed(docs)

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)

        index.add(
            np.array(embeddings).astype("float32")
        )

        self.index = index

    def save(self):

        faiss.write_index(
            self.index,
            "data/faiss.index"
        )

        with open(
            "data/documents.pkl",
            "wb"
        ) as f:

            pickle.dump(
                self.documents,
                f
            )

    def load(self):

        self.index = faiss.read_index(
            "data/faiss.index"
        )

        with open(
            "data/documents.pkl",
            "rb"
        ) as f:

            self.documents = pickle.load(f)

    def search(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.embedder.embed(
            [query]
        )

        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"),
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append(
                    self.documents[idx]
                )

        return results