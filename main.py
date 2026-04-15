import json
import numpy as np
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from db import SessionLocal
from models import Destination

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open("dest.json", "r") as file:
    destinations = json.load(file)

db = SessionLocal()

if db.query(Destination).count() == 0:
    for d in destinations:
        text = f"{d['name']} {d['country']} {d['description']} {d['category']}"
        embedding = model.encode(text)

        emb_bytes = np.array(embedding).astype(np.float32).tobytes()

        dest = Destination(
            name=d["name"],
            country=d["country"],
            description=d["description"],
            category=d["category"],
            embedding=emb_bytes
        )

        db.add(dest)

    db.commit()


def search(user_input):
    user_embedding = model.encode([f"travel destination {user_input}"])

    results = []
    all_data = db.query(Destination).all()

    for d in all_data:
        emb = np.frombuffer(d.embedding, dtype=np.float32)
        score = cosine_similarity(user_embedding, [emb])[0][0]
        results.append((d, score))

    results.sort(key=lambda x: x[1], reverse=True)

    if len(results) == 0:
        return []

    top_results = results[:3]

    for d, score in results:
        print(f"{d.name}: {score:.4f}")

    if top_results[0][1] < 0.3:
        return [d for d, _ in random.sample(results, min(3, len(results)))]

    return [d for d, _ in top_results]


