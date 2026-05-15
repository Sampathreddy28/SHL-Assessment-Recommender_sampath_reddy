OFF_TOPIC_KEYWORDS = [
    "weather",
    "football",
    "movie",
    "bitcoin",
    "recipe",
    "politics",
    "medical",
    "legal",
]


PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "bypass",
    "override instructions",
]


def is_off_topic(text: str) -> bool:

    text = text.lower()

    return any(
        keyword in text
        for keyword in OFF_TOPIC_KEYWORDS
    )


def is_prompt_injection(text: str) -> bool:

    text = text.lower()

    return any(
        pattern in text
        for pattern in PROMPT_INJECTION_PATTERNS
    )