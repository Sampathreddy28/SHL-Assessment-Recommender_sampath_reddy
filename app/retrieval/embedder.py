from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class Embedder:

    def __init__(self):

        self.model = SentenceTransformer(MODEL_NAME)

    def embed(self, texts):

        return self.model.encode(
            texts,
            convert_to_numpy=True
        )