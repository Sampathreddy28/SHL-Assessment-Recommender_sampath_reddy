from pathlib import Path

from app.agent.conversation import (
    extract_user_context,
    needs_clarification,
    is_comparison_request,
    is_refinement,
)

from app.agent.guardrails import (
    is_off_topic,
    is_prompt_injection,
)

from app.agent.llm import (
    generate_response
)

from app.retrieval.search import (
    AssessmentSearchEngine
)


SYSTEM_PROMPT = Path(
    "app/prompts/system_prompt.txt"
).read_text(encoding="utf-8")


class RecommendationAgent:

    def __init__(self):

        self.search_engine = (
            AssessmentSearchEngine()
        )

    def build_search_query(
        self,
        messages
    ):

        query_parts = []

        for msg in messages:

            if msg.role != "user":
                continue

            query_parts.append(
                msg.content
            )

        return " ".join(query_parts)

    def format_catalog_context(
        self,
        results
    ):

        context = []

        for item in results:

            context.append(
                f"""
                Name: {item['name']}
                Type: {item['test_type']}
                Skills: {', '.join(item['skills'])}
                Description: {item['description']}
                URL: {item['url']}
                """
            )

        return "\n".join(context)

    def handle_chat(self, messages):

        user_context = extract_user_context(
            messages
        )

        # Prompt injection refusal
        if is_prompt_injection(user_context):

            return {
                "reply": (
                    "I can only assist with "
                    "SHL assessment recommendations."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # Off-topic refusal
        if is_off_topic(user_context):

            return {
                "reply": (
                    "I only support SHL "
                    "assessment recommendation "
                    "conversations."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # Clarification behavior
        if needs_clarification(user_context):

            clarification_reply = generate_response(
                SYSTEM_PROMPT,
                f"""
                User request:
                {user_context}

                Ask a concise clarification question.
                """
            )

            return {
                "reply": clarification_reply,
                "recommendations": [],
                "end_of_conversation": False
            }

        # Build full conversational query
        search_query = self.build_search_query(
            messages
        )

        top_k = 5

        # Refinement behavior
        if is_refinement(user_context):
            top_k = 7

        # Comparison behavior
        if is_comparison_request(user_context):
            top_k = 2

        # Semantic retrieval
        results = (
            self.search_engine
            .search_assessments(
                search_query,
                top_k=top_k
            )
        )

        # Format retrieval context for LLM
        catalog_context = (
            self.format_catalog_context(
                results
            )
        )

        # LLM grounded response
        llm_reply = generate_response(
            SYSTEM_PROMPT,
            f"""
            User conversation:
            {search_query}

            Retrieved SHL catalog data:
            {catalog_context}

            Generate a grounded response using ONLY the retrieved catalog data.
            """
        )

        recommendations = []

        seen = set()

        for item in results:

            if item["url"] in seen:
                continue

            seen.add(item["url"])

            # Safety check for valid SHL URLs
            if (
                item["url"].startswith(
                    "https://www.shl.com/"
                )
            ):

                recommendations.append({
                    "name": item["name"],
                    "url": item["url"],
                    "test_type": item["test_type"]
                })

        # Hard evaluator limit
        recommendations = recommendations[:10]

        # Empty recommendation handling
        if len(recommendations) == 0:

            return {
                "reply": (
                    "I could not find suitable "
                    "SHL assessments for the "
                    "provided requirements."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        return {
            "reply": llm_reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }