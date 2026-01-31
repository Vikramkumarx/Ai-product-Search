import gradio as gr
import json
import time

# --- IMPORT BACKEND ---
try:
    from lambda_handler import lambda_handler
except ImportError:
    lambda_handler = None

# --- EXPERT SEARCH LOGIC ---
def expert_search(query_text, min_p, max_p, cat):
    start = time.time()
    if not query_text: return "Please enter a product name.", ""
    
    event = {
        "query": query_text,
        "min_price": min_p,
        "max_price": max_p,
        "category": cat
    }
    
    results = []
    if lambda_handler:
        try:
            resp = lambda_handler(event, None)
            if resp.get('statusCode') != 200:
                return f"Error: {resp.get('body')}", ""
            results = json.loads(resp['body'])
        except Exception as e:
            return f"Error: {str(e)}", ""
    else:
        results = [{"error": "Backend Disconnected"}]
        
    dur = round(time.time() - start, 2)
    html = generate_expert_cards(results)
    
    if not results:
        return f"No expert matches for '{query_text}'.", html
        
    return f"Found {len(results)} expert recommendations in {dur}s.", html

def generate_expert_cards(results):
    html = "<div style='display: flex; flex-direction: column; gap: 15px;'>"
    if not isinstance(results, list): return str(results)
    
    for idx, item in enumerate(results):
        name = item.get('product_name', 'Unknown')
        price = int(item.get('price', 0)) # FORCE INT
        specs = item.get('specifications', 'No Specs')
        rating = item.get('rating', 0)
        score = item.get('score', 0)
        
        # UI Logic
        badge = ""
        border_color = "#ddd"
        bg_color = "white"
        
        if idx == 0:
            badge = "<div style='background: #FFD700; color: #000; font-weight: bold; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 8px;'>🏆 AI BEST CHOICE</div>"
            border_color = "#FFD700"
            bg_color = "#fffbe6"
        elif rating >= 4.5:
             badge = "<div style='background: #2ecc71; color: white; font-size: 11px; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px;'>★ TOP RATED</div>"
        
        # High Contrast Specification Pills
        spec_list = specs.split("|")
        # Bold text, Darker background pill
        spec_html = "".join([f"<span style='background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-right: 8px; display:inline-block; margin-bottom:4px;'>{s.strip()}</span>" for s in spec_list])

        html += f"""
        <div style="border: 2px solid {border_color}; background: {bg_color}; padding: 18px; border-radius: 10px; display: flex; justify-content: space-between; align_items: start; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="flex: 3;">
                {badge}
                <h2 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 20px;">{name}</h2>
                <div style="margin-top: 8px;">{spec_html}</div>
            </div>
            <div style="flex: 1; text-align: right; min-width: 120px;">
                <div style="font-size: 24px; font-weight: 800; color: #2c3e50;">₹{price:,}</div>
                <div style="color: #f39c12; font-size: 16px; margin-top: 5px; font-weight: bold;">★ {rating} / 5.0</div>
                <div style="font-size: 11px; color: #7f8c8d; margin-top: 5px;">Match: {int(score*100)}%</div>
            </div>
        </div>
        """
    html += "</div>"
    return html

# --- CHATBOT LOGIC ---
def chat_response(message, history):
    # Reuse Search to get context
    results = []
    if lambda_handler:
        resp = lambda_handler({"query": message}, None)
        if resp.get('statusCode') == 200:
            results = json.loads(resp['body'])
    
    if not results:
        return "Sorry, I couldn't find any products related to that. Try searching for Laptops, Phones, or FMCG items."
    
    top = results[0]
    return f"Based on your request, I recommend the **{top['product_name']}** (₹{int(top['price']):,}).\n\nIt features: {top['specifications']}.\n\nIs there anything specific you are looking for in terms of specs or price?"

# --- UI ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), title="AI Product Expert") as demo:
    gr.Markdown("# 🧠 AI Product Expert System")
    
    with gr.Tabs():
        # TAB 1: EXPERT SEARCH
        with gr.Tab("🔍 Expert Search"):
            gr.Markdown("Type what you are looking for. AI will analyze thousands of specs to find the best match.")
            with gr.Row():
                with gr.Column(scale=1):
                    txt_in = gr.Textbox(label="Your Requirement", placeholder="e.g. Best Laptop under 1 Lakh for Coding")
                    btn_find = gr.Button("Find Best Product", variant="primary")
                    
                    with gr.Accordion("Advanced Filters", open=True):
                        p_min = gr.Slider(0, 300000, value=0, label="Min Price (₹)")
                        p_max = gr.Slider(0, 300000, value=300000, label="Max Price (₹)")
                        cat_dd = gr.Dropdown(["All", "Electronics", "Fashion", "Groceries"], value="All", label="Category")

                with gr.Column(scale=2):
                    lbl_stat = gr.Textbox(label="AI Analysis Status", interactive=False)
                    html_res = gr.HTML(label="Expert Recommendations")
            
            btn_find.click(expert_search, [txt_in, p_min, p_max, cat_dd], [lbl_stat, html_res])

        # TAB 2: CHATBOT
        with gr.Tab("💬 AI Assistant"):
            gr.Markdown("### Ask me anything about our products!")
            gr.ChatInterface(fn=chat_response)

    # --- FOOTER ---
    gr.Markdown("""
    <div style="text-align: center; margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; color: #666;">
        <p>Developed by <b>Vikram Kumar</b></p>
        <p>📧 Vikram10072003@gmail.com | 🔗 <a href="https://www.linkedin.com/in/vikram-kumar-51b9a1247" target="_blank">LinkedIn Profile</a></p>
    </div>
    """)

if __name__ == "__main__":
    import os
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)), share=True)
