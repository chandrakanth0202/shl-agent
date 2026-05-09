from app.services.semantic_search import semantic_recommend

query = "experienced backend engineer coding assessment"

results = semantic_recommend(query)

for item in results:
    print(item["name"], item["similarity"])