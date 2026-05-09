from app.services.recommender import recommend_assessments
from app.services.semantic_search import semantic_recommend

def hybrid_recommend(query: str):

    keyword_results = recommend_assessments(query)

    semantic_results = semantic_recommend(query)

    combined = []

    added_names = set()

    # keyword results first
    for item in keyword_results:

        combined.append(item)

        added_names.add(item["name"])

    # semantic results next
    for item in semantic_results:

        if item["name"] not in added_names:

            combined.append(item)

            added_names.add(item["name"])

    return combined[:10]