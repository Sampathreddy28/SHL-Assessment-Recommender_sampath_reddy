import json
from pathlib import Path


CATALOG_PATH = Path(
    "data/catalog.json"
)


class AssessmentSearchEngine:

    def __init__(self):

        with open(
            CATALOG_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            self.catalog = json.load(f)

    def score_assessment(
        self,
        assessment,
        query
    ):

        query = query.lower()

        text = " ".join([
            assessment.get("name", ""),
            assessment.get("description", ""),
            " ".join(
                assessment.get("skills", [])
            )
        ]).lower()

        score = 0

        for word in query.split():

            if word in text:
                score += 1

        return score

    def search_assessments(
        self,
        query,
        top_k=5
    ):

        scored = []

        for item in self.catalog:

            score = self.score_assessment(
                item,
                query
            )

            scored.append(
                (score, item)
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        results = [
            item
            for score, item in scored
            if score > 0
        ]

        return results[:top_k]