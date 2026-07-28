import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Step 1: Load your Q&A data
df = pd.read_csv("data/qa_data.csv")
questions = df["question"].tolist()
answers = df["answer"].tolist()

# Step 2: Load the embedding model (converts text to numbers)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 3: Convert all questions into embeddings (numbers)
question_embeddings = model.encode(questions)

print("Data loaded:", len(questions), "questions")
print("Embeddings shape:", question_embeddings.shape)
# Step 4: Build a FAISS index (this is like creating a search engine for your questions)
dimension = question_embeddings.shape[1]  # this will be 384
index = faiss.IndexFlatL2(dimension)
index.add(np.array(question_embeddings))

print("FAISS index built with", index.ntotal, "questions")

# Step 5: Try a test search
user_query = "leaves are yellow"
query_embedding = model.encode([user_query])

distances, indices = index.search(np.array(query_embedding), k=1)  # k=1 means "find top 1 match"

best_match_index = indices[0][0]
print("\nUser asked:", user_query)
print("Best matching question in your data:", questions[best_match_index])
print("Answer:", answers[best_match_index])