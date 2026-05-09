from app.services.faiss_search import faiss_recommend

query = "experienced backend engineer coding test"

results = faiss_recommend(query)

for item in results:

    print(item["name"])