def generate_reply(conversation_text: str, recommendations):

    if not recommendations:

        return "I could not find suitable SHL assessments for the provided requirements."

    assessment_names = []

    for item in recommendations:

        assessment_names.append(item["name"])

    joined_names = ", ".join(assessment_names)

    return (
        f"Based on your hiring requirements, "
        f"the following SHL assessments are recommended: "
        f"{joined_names}."
    )