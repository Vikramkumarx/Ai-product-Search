import sqlite3
import pandas as pd
from sentence_transformers import SentenceTransformer
import json
import os

DB_FILE = 'product_search.db'
CSV_FILE = 'products.csv'

def embed_products():
    print("Loading Expert Model (All-MiniLM-L6-v2) for Text-Only Precision...")
    # Switched back to text-optimized model as we dropped images
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    
    # Read CSV
    df = pd.read_csv(CSV_FILE)
    
    # Connect DB (Reset)
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Read Schema
    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())
        
    print("Embedding Specifications...")
    vectors = []
    
    # Embedding Strategy: Name + Category + Specifications
    # This ensures "Laptop 16GB RAM" matches query "16gb laptop"
    texts_to_embed = df.apply(lambda x: f"{x['product_name']} {x['category']} {x['specifications']}", axis=1).tolist()
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    
    data_to_insert = []
    for idx, row in df.iterrows():
        vec_json = json.dumps(embeddings[idx].tolist())
        data_to_insert.append((
            row['product_id'],
            row['product_name'],
            row['category'],
            row['price'],
            row['rating'],
            row['specifications'], # New Column
            vec_json
        ))
        
    cursor.executemany('''
        INSERT INTO products_vectors (product_id, product_name, category, price, rating, specifications, vector)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data_to_insert)
    
    conn.commit()
    conn.close()
    print("Expert Database Ready!")

if __name__ == "__main__":
    embed_products()
