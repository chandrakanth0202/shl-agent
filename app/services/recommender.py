import json
from app.services.extractor import extract_seniority

def load_catalog():

    with open("app/data/shl_catalog.json", "r") as file:
        return json.load(file)

def recommend_assessments(conversation_text: str):


    catalog = load_catalog()

    conversation_text = conversation_text.lower()
    detected_level = extract_seniority(conversation_text)

    results = []

    for assessment in catalog:

        score = 0

        skills = [skill.lower() for skill in assessment["skills"]]

        # Strong exact matching
        if "java" in conversation_text and "java" in skills:
            score += 5

        if "python" in conversation_text and "python" in skills:
            score += 5

        if "personality" in conversation_text and "personality" in skills:
            score += 5

        if "behavior" in conversation_text and "behavior" in skills:
            score += 5

        if "cognitive" in conversation_text and "cognitive" in skills:
            score += 5

        if "reasoning" in conversation_text and "reasoning" in skills:
            score += 5

        # weaker generic match
        if "backend" in conversation_text and "backend" in skills:
            score += 1
        # seniority matching
        if detected_level:

            if assessment["level"].lower() == detected_level.lower():
                score += 3

        if score > 0:

            assessment_copy = assessment.copy()

            assessment_copy["score"] = score

            results.append(assessment_copy)

    # sort highest relevance first
       # sort highest relevance first
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    # Keep only strong matches if available
    strong_results = [
        item for item in results
        if item["score"] >= 5
    ]

    if strong_results:
        results = strong_results

    # remove score before returning
    for item in results:
        item.pop("score", None)

    return results[:10]