from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

model = None
catalog = None
catalog_embeddings = None

def load_model():

    global model
    global catalog
    global catalog_embeddings

    if model is not None:
        return

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("app/data/shl_catalog.json", "r") as file:
        catalog = json.load(file)

    catalog_texts = [

        item.get("name", "") + " " +
        item.get("description", "")

        for item in catalog
    ]

    catalog_embeddings = model.encode(catalog_texts)

def semantic_recommend(query: str):

    load_model()

    query_embedding = model.encode([query])

    similarities = cosine_similarity(
        query_embedding,
        catalog_embeddings
    )[0]

    ranked_indices = np.argsort(similarities)[::-1]

    results = []

    for index in ranked_indices[:3]:

        item = catalog[index].copy()

        item["similarity"] = float(similarities[index])

        results.append(item)

    return results