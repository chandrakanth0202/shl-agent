import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

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

# generate embeddings
embeddings = model.encode(catalog_texts)

# convert to numpy float32
embeddings = np.array(embeddings).astype("float32")

# create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

def faiss_recommend(query: str):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, 3)

    results = []

    for idx in indices[0]:

        results.append(catalog[idx])

    return results