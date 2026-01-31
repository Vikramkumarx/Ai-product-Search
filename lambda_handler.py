import json
import os
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'
_model_cache = None

def get_model():
    global _model_cache
    if _model_cache is None:
        print(f"Lazy Loading Model: {MODEL_NAME}...")
        try:
            _model_cache = SentenceTransformer(MODEL_NAME)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return _model_cache

# Use Absolute Path for Cloud Compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'product_search.db')

def get_db_connection():
    if not os.path.exists(DB_FILE):
        print(f"CRITICAL ERROR: DB File not found at {DB_FILE}")
        return None
    return sqlite3.connect(DB_FILE)

def cosine_similarity(v1, v2):
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0: return 0
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def lambda_handler(event, context):
    try:
        print(f"--- Expert Search: {event.get('query')} ---")
        
        if not os.path.exists(DB_FILE):
             print("DB Not Found")
             return {'statusCode': 500, 'body': json.dumps({'error': 'Database not found. Run embed_products.py'})}

        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Search Params
        query_text = event.get('query', '')
        min_price = float(event.get('min_price', 0))
        max_price = float(event.get('max_price', 1000000)) 
        category_filter = event.get('category', None)
        
        # Enhance Query with "Best" logic if user didn't specify
        # (Implicitly looking for high quality)
        search_query = query_text
        
        # Encode
        query_vector = None
        model = get_model()
        if search_query and model:
            query_vector = model.encode(search_query)

        # Vector Search
        candidates = []
        if query_vector is not None:
            sql = "SELECT * FROM products_vectors"
            params = []
            if category_filter and category_filter != "All":
                sql += " WHERE category = ?"
                params.append(category_filter)
            cursor.execute(sql, params)
            all_rows = cursor.fetchall()
            
            for row in all_rows:
                # Price Filter
                if not (min_price <= row['price'] <= max_price): continue
                
                p_vec = np.array(json.loads(row['vector']))
                
                # Similarity Score
                sim_score = cosine_similarity(query_vector, p_vec)
                
                # Expert Score Logic:
                # 70% Semantic Match + 30% Product Rating
                # This ensures "Best" products float to top
                rating_score = row['rating'] / 5.0 # Normalize 0-1
                final_score = (sim_score * 0.7) + (rating_score * 0.3)
                
                item = dict(row)
                item['score'] = float(final_score)
                item['match_type'] = 'Exact Match' if sim_score > 0.8 else 'expert_recommendation'
                candidates.append(item)
                
            # Sort by Expert Score
            candidates.sort(key=lambda x: x['score'], reverse=True)
            top_results = candidates[:20]

            # Clean response (remove vector)
            for item in top_results: 
                if 'vector' in item: del item['vector']
            
            print(f"Returning {len(top_results)} expert results.")
            return {'statusCode': 200, 'body': json.dumps(top_results, default=str)}
        
        return {'statusCode': 200, 'body': json.dumps([])}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
