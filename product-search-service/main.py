import faiss
import pickle
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# These paths are relative to the WORKDIR /app in the container
INDEX_PATH = "products.index"
DATA_PATH = "products_data.pkl"

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index(INDEX_PATH)
with open(DATA_PATH, 'rb') as f:
    products_data = pickle.load(f)

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

@app.post("/search")
def search(search_query: SearchQuery):
    query_embedding = model.encode([search_query.query])
    query_embedding = np.array(query_embedding).astype('float32')
    
    _, indices = index.search(query_embedding, search_query.top_k)
    
    results = [products_data[i] for i in indices[0]]
    return results