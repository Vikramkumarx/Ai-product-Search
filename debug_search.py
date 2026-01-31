import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer

DB_FILE = 'product_search.db'

def test_search():
    print(f"--- DEBUGGING SEARCH ---")
    
    # 1. Check DB Connection & Count
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM products_vectors")
        count = cursor.fetchone()[0]
        print(f"Total Products in DB: {count}")
        
        if count == 0:
            print("CRITICAL: Database is empty!")
            return
            
        # 2. Check Sample Data
        cursor.execute("SELECT product_name, price, category FROM products_vectors LIMIT 3")
        print("\nSample Products:")
        for row in cursor.fetchall():
            print(f"- {row[0]} (₹{row[1]}) [{row[2]}]")

        # 3. Test Keyword Search
        query = "nike" # Lowercase test
        print(f"\nTesting Keyword Search for '{query}'...")
        # SQLite LIKE is usually case-insensitive, but let's verify
        cursor.execute("SELECT product_name, price FROM products_vectors WHERE product_name LIKE ?", (f"%{query}%",))
        results = cursor.fetchall()
        print(f"Found {len(results)} matches via SQL LIKE.")
        for r in results[:3]: print(f"  Match: {r[0]} - ₹{r[1]}")
        
        # 4. Filter Check (Price)
        print(f"\nChecking Price Distribution for '{query}'...")
        cursor.execute("SELECT min(price), max(price) FROM products_vectors WHERE product_name LIKE ?", (f"%{query}%",))
        min_p, max_p = cursor.fetchone()
        print(f"  Price Range: ₹{min_p} - ₹{max_p}")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    test_search()
