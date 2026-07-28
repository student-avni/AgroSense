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
