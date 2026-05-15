REFINEMENT_KEYWORDS = [
    "also",
    "add",
    "include",
    "instead",
    "actually",
    "change",
]


def extract_user_context(messages):

    user_messages = []

    for msg in messages:

        if msg.role == "user":

            user_messages.append(
                msg.content
            )

    return " ".join(user_messages)


def needs_clarification(user_text: str) -> bool:

    user_text = user_text.strip()

    return len(user_text.split()) < 4


def is_comparison_request(text: str) -> bool:

    text = text.lower()

    comparison_words = [
        "compare",
        "difference",
        "vs",
        "versus",
    ]

    return any(
        word in text
        for word in comparison_words
    )


def is_refinement(text: str) -> bool:

    text = text.lower()

    return any(
        keyword in text
        for keyword in REFINEMENT_KEYWORDS
    )