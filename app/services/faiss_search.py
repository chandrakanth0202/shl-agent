import json
import numpy as np
import faiss

model = None
catalog = None
index = None

def load_faiss():

    global model
    global catalog
    global index

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

    embeddings = model.encode(catalog_texts)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

def faiss_recommend(query: str):

    load_faiss()

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, 3)

    results = []

    for idx in indices[0]:

        results.append(catalog[idx])

    return results