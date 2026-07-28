import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Step 1: Load your Q&A data
df = pd.read_csv("data/qa_data.csv")
questions = df["question"].tolist()
answers = df["answer"].tolist()

# Step 2: Load the embedding model (converts text to numbers)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 3: Convert all questions into embeddings
question_embeddings = embedding_model.encode(questions)

# Step 4: Build FAISS search index
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(question_embeddings))

# Step 5: Function that does the full RAG process
def get_answer(user_query):
    # Retrieval: find the most similar question in our data
    query_embedding = embedding_model.encode([user_query])
    distances, indices = index.search(np.array(query_embedding), k=1)
    best_match_index = indices[0][0]
    retrieved_answer = answers[best_match_index]
    retrieved_question = questions[best_match_index]

    # Generation: send retrieved info to Gemini to write a natural answer
    gemini_model = genai.GenerativeModel("gemini-flash-latest")
    prompt = f"""You are a helpful farming assistant. A farmer asked: "{user_query}"

Based on our knowledge base, here is relevant information:
Question: {retrieved_question}
Answer: {retrieved_answer}

Using this information, give a clear, friendly, helpful answer to the farmer in simple language."""

    response = gemini_model.generate_content(prompt)
    return response.text

# Test it
if __name__ == "__main__":
    test_query = "leaves are yellow"
    result = get_answer(test_query)
    print("User asked:", test_query)
    print("AI Answer:", result)