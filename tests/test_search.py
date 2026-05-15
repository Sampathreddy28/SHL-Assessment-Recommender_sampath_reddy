from app.retrieval.search import (
    AssessmentSearchEngine
)


engine = AssessmentSearchEngine()

results = engine.search_assessments(
    "Java developer with communication skills",
    top_k=5
)

for idx, item in enumerate(results, start=1):

    print("\n")
    print("=" * 50)

    print(f"Result {idx}")

    print("Name:", item["name"])

    print("Type:", item["test_type"])

    print("Skills:", item["skills"])

    print("URL:", item["url"])