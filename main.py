import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

with open("dest.json", "r") as file:
   destinations = json.load(file)

df = pd.DataFrame(destinations)

df['text'] = df['name'] + " " + df['country'] + " " + df['description'] + " " + df['category']

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

df['embedding'] = df['text'].apply(lambda x: model.encode(x).tolist())

def find_similar(user_input, df):
   user_embedding = model.encode([user_input])
   similarities = cosine_similarity(user_embedding, list(df['embedding']))
   sorted_indices = similarities[0].argsort()[::-1]
   results = []
   for i in sorted_indices[:3]:
       results.append(df.iloc[i]['name'])
   return results

query = input("Where do you want to travel? ")

results = find_similar(query, df)

print("\nTop 3 recommendations:")
for r in results:
   print(r)