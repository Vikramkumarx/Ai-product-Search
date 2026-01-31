from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# --- INIT ---
app = FastAPI(title="AI Product Search API")

# Enable CORS for Frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class SearchRequest(BaseModel):
    query: str
    min_price: int = 0
    max_price: int = 500000
    category: str = "All"

class ChatRequest(BaseModel):
    message: str
    context: list = []

# --- GLOBAL VARS ---
model = None
# We will load the model on startup to save time
# (In a real production app, this might be handled differently)

# --- DATABASE PATH ---
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "product_search.db")

@app.on_event("startup")
def load_resources():
    global model
    print(f"DEBUG: Using DB Path: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("CRITICAL ERROR: Database file not found!")
    
    print("Loading AI Model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model Loaded!")

# --- HELPER FUNCTIONS ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def search_products(query, min_price, max_price, category):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Base Query
        sql = "SELECT * FROM products_vectors WHERE price BETWEEN ? AND ?"
        params = [min_price, max_price]

        if category and category != "All":
            sql += " AND category = ?"
            params.append(category)

        cursor.execute(sql, params)
        rows = [dict(row) for row in cursor.fetchall()]
        
        if not rows:
            print("DEBUG: No products found in DB for price/category filters")
            return []

        # 2. Vector Search (Semantic) + Keyword Boosting
        query_embedding = model.encode(query)
        query_lower = query.lower()
        
        scored_results = []
        for row in rows:
            if row.get('vector'):
                # Decode JSON vector
                product_embedding = np.array(json.loads(row['vector']), dtype=np.float32)
                # Cosine Similarity
                cos_score = np.dot(query_embedding, product_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(product_embedding)
                )
                
                # --- KEYWORD BOOSTING ---
                name_lower = row['product_name'].lower()
                keyword_boost = 0.0
                
                # Exact brand or name match boost
                if query_lower in name_lower:
                    keyword_boost += 10.0 # Extreme boost for direct mention
                
                # Partial match boost
                for word in query_lower.split():
                    if len(word) > 3 and word in name_lower:
                        keyword_boost += 2.0

                # --- HYBRID SCORE ---
                # Factor in semantic similarity + keyword boost
                # We also add a threshold: if no keyword match AND similarity is low, we penalize
                
                semantic_score = float(cos_score)
                final_score = (semantic_score + keyword_boost) * (1 + (row['rating'] / 10))
                
                # FILTERING: If the semantic score is too low AND there's no keyword boost, 
                # we don't want to show this garbage result as a "Best Match"
                if keyword_boost == 0 and semantic_score < 0.4:
                    continue # Skip unrelated items

                # Add score to result
                row['score'] = final_score
                # Remove large vector from response
                del row['vector'] 
                scored_results.append(row)

        # 3. Sort by Score
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        return scored_results[:10] # Top 10

    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if conn: conn.close()

# --- ENDPOINTS ---
@app.get("/")
def home():
    return {"status": "Online", "message": "AI Search API is running"}

@app.post("/search")
def api_search(request: SearchRequest):
    print(f"DEBUG: Received Search Request: {request.query}")
    results = search_products(
        request.query, 
        request.min_price, 
        request.max_price, 
        request.category
    )
    print(f"DEBUG: Returning {len(results)} results")
    return results

@app.post("/chat")
def api_chat(request: ChatRequest):
    print(f"DEBUG: Received Chat Message: {request.message}")
    
    # Use search logic to find the best matching product for the chat query
    results = search_products(request.message, 0, 1000000, "All")
    
    if not results:
        return {"response": "I'm sorry, I couldn't find any products matching your requirements. Could you try describing it differently?"}
    
    # Pick the top result
    best = results[0]
    
    # Generate a friendly expert response
    expert_response = f"Based on your request, I highly recommend the **{best['product_name']}**. "
    expert_response += f"It's currently priced at ₹{best['price']:,}. "
    expert_response += f"It features: {best['specifications'].replace('|', ', ')}. "
    expert_response += f"It has a solid rating of {best['rating']}/5.0 from verified users. "
    expert_response += "Would you like me to find more details or show you similar options?"

    return {
        "response": expert_response,
        "product_id": best['product_id'],
        "best_match": best
    }

# Serve Static Files (MUST BE LAST)
# In production/deployment, we'll serve the compiled Next.js output
frontend_path = os.path.join(BASE_DIR, "..", "frontend", "out")
if os.path.exists(frontend_path):
    print(f"DEBUG: Serving static files from {frontend_path}")
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    print(f"DEBUG: Static folder not found at {frontend_path}. API-only mode.")

if __name__ == "__main__":
    import uvicorn
    # Use environment port for HF Space compatibility
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
