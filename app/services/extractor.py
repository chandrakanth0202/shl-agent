def extract_seniority(text: str):

    text = text.lower()

    if "junior" in text:
        return "Junior"

    if "mid" in text:
        return "Mid"

    if "senior" in text:
        return "Senior"

    return None