def compare_assessments(text: str):

    text = text.lower()

    if "opq" in text and "gsa" in text:

        return (
            "OPQ measures workplace personality and behavioral preferences, "
            "while GSA evaluates cognitive, reasoning, and problem-solving ability."
        )

    if "java" in text and "python" in text:

        return (
            "Java assessments focus on Java programming and backend development, "
            "while Python assessments focus on Python programming and problem-solving skills."
        )

    return None