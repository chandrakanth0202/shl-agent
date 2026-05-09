def detect_prompt_injection(text: str):

    text = text.lower()

    blocked_phrases = [

        "ignore previous instructions",
        "forget previous instructions",
        "jailbreak",
        "hack",
        "system prompt",
        "recommend hackerrank",
        "recommend leetcode",
        "recommend codility"

    ]

    off_topic = [

        "salary",
        "legal advice",
        "visa",
        "immigration",
        "politics"

    ]

    for phrase in blocked_phrases:

        if phrase in text:
            return True

    for phrase in off_topic:

        if phrase in text:
            return True

    return False