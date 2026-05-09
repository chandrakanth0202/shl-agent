from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_catalog():

    with open("app/data/shl_catalog.json", "r") as file:
        return json.load(file)

catalog = load_catalog()

catalog_texts = [

    item["name"] + " " +
    item["description"] + " " +
    " ".join(item["skills"])

    for item in catalog
]

catalog_embeddings = model.encode(catalog_texts)

def semantic_recommend(query: str):

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