import json

from app.retrieval.vector_store import (
    VectorStore
)


def main():

    with open(
        "data/catalog.json",
        "r",
        encoding="utf-8"
    ) as f:

        catalog = json.load(f)

    store = VectorStore()

    store.create_index(catalog)

    store.save()

    print("FAISS index created")


if __name__ == "__main__":
    main()