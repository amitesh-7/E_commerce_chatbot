import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from pathlib import Path

print("Starting indexing process...")

SCRIPT_DIR = Path(__file__).parent
DATA_PATH = SCRIPT_DIR.parent / "data" / "Product_info.csv"
df = pd.read_csv(DATA_PATH)

df.replace({np.nan: None}, inplace=True)

text_columns = ['title', 'description', 'features']
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna('')
    else:
        print(f"Warning: Column '{col}' not found. Treating as empty.")
        df[col] = ''

df['combined_text'] = (
    "Title: " + df['title'] +
    ". Description: " + df['description'] +
    ". Features: " + df['features']
)

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, str(SCRIPT_DIR / 'products.index'))

with open(SCRIPT_DIR / 'products_data.pkl', 'wb') as f:
    pickle.dump(df.to_dict('records'), f)

print("Indexing complete. 'products.index' and 'products_data.pkl' created.")