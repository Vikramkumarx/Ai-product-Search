import csv
import random

def get_price(name, category):
    name = name.lower()
    
    # --- Electronics (Laptops/PCs) ---
    if 'macbook air' in name: return random.randint(65000, 95000)
    if 'macbook pro' in name: return random.randint(159900, 250000)
    if 'xps' in name: return random.randint(120000, 180000)
    if 'alienware' in name: return random.randint(150000, 280000)
    if 'spectre' in name: return random.randint(130000, 170000)
    if 'thinkpad' in name: return random.randint(90000, 160000)
    if 'legion' in name: return random.randint(110000, 160000)
    if 'zephyrus' in name: return random.randint(140000, 200000)
    if 'victus' in name: return random.randint(58000, 85000)
    if 'tuf gaming' in name: return random.randint(55000, 80000)
    if 'predator' in name: return random.randint(90000, 150000)
    if 'nitro' in name: return random.randint(55000, 85000)
    if 'titan' in name: return random.randint(250000, 400000)
    if 'stealth' in name: return random.randint(150000, 250000)
    
    # --- Electronics (Phones) ---
    if 'iphone 15' in name: return random.randint(72000, 150000)
    if 'iphone 14' in name: return random.randint(58000, 70000)
    if 'iphone 13' in name: return random.randint(48000, 55000)
    if 'pixel 8' in name: return random.randint(70000, 85000)
    if 'pixel 7' in name: return random.randint(45000, 55000)
    if 's23 ultra' in name: return random.randint(95000, 115000)
    if 'z fold' in name: return random.randint(130000, 160000)
    if 'oneplus' in name: return random.randint(35000, 65000)
    if 'realme' in name: return random.randint(15000, 35000)
    if 'xiaomi' in name: return random.randint(12000, 40000)
    
    # --- Electronics (Audio/Video/Photo/Watches) ---
    if 'alpha' in name: return random.randint(180000, 250000)
    if 'lumix' in name: return random.randint(70000, 150000)
    if 'hd 660' in name: return random.randint(35000, 45000)
    if 'flip 6' in name: return random.randint(9000, 12000)
    if 'boombox' in name: return random.randint(25000, 35000)
    if 'wh-1000xm5' in name: return random.randint(24000, 29000)
    if 'fastrack' in name: return random.randint(1500, 5000)
    if 'titan' in name: return random.randint(3000, 15000)
    if 'casio' in name: return random.randint(2000, 25000)
    if 'fossil' in name: return random.randint(8000, 18000)
    
    # --- Fashion ---
    if '501' in name: return random.randint(3500, 6000) # Levi's
    if 'oversized' in name: return random.randint(800, 2500) # H&M/Zara
    if 'leather' in name: return random.randint(4000, 8000)
    if 'running' in name: return random.randint(2000, 15000)
    if 'bata' in name: return random.randint(800, 3500)
    
    # --- Groceries ---
    if 'maggi' in name: return random.randint(15, 150)
    if 'ketchup' in name: return random.randint(100, 250)
    if 'biscuit' in name: return random.randint(20, 100)
    if 'coffee' in name: return random.randint(300, 800)
    if 'ghee' in name: return random.randint(500, 800)

    # Generic Fallbacks (Safety Net)
    if category == 'Electronics': return random.randint(50000, 100000) # SAFE HIGH DEFAULT
    if category == 'Fashion': return random.randint(1000, 4000)
    return random.randint(100, 500)

def get_specs(category, name):
    name_lower = name.lower()
    specs = []
    
    # --- Specs Mapping ---
    if any(x in name_lower for x in ['macbook', 'ideapad', 'thinkpad', 'xps', 'inspiron', 'pavilion', 'spectre', 'victus', 'vivobook', 'zenbook', 'legion', 'alienware', 'tuf', 'g15']):
        proc = "Intel i5 12th Gen"
        if any(x in name_lower for x in ['pro', 'xps', 'spectre', 'alienware', 'legion', 'zenbook', 'macbook pro']): proc = "Intel i7 13th Gen / M2 Pro"
        elif 'm1' in name_lower: proc = "Apple M1 Chip"
        elif 'm2' in name_lower: proc = "Apple M2 Chip"
        elif 'victus' in name_lower or 'tuf' in name_lower: proc = "Ryzen 7 5800H"
        
        ram = "16GB RAM"
        storage = "1TB SSD" if 'pro' in name_lower or 'alienware' in name_lower else "512GB SSD"
        screen = "16-inch 165Hz" if 'gaming' in name_lower or 'legion' in name_lower or 'victus' in name_lower else "15.6-inch FHD"
        
        specs = [f"Processor: {proc}", ram, storage, f"Display: {screen}"]

    elif any(x in name_lower for x in ['iphone', 'galaxy', 'xperia', 'oneplus']):
        cam = "50MP Main"
        if 'ultra' in name_lower: cam = "200MP Main / 100x Zoom"
        chip = "A16 Bionic" if 'iphone' in name_lower else "Snapdragon 8 Gen 2"
        specs = [f"Camera: {cam}", f"Chip: {chip}", "Battery: 5000mAh", "5G Supported"]

    elif 'alpha' in name_lower: specs = ["Sensor: Full Frame CMOS", "Video: 4K 60p", "Focus: Real-time Eye AF", "Conn: WiFi/NFC"]
    elif 'eos' in name_lower: specs = ["Sensor: APS-C/Full Frame", "Video: 4K", "Lens: Kit Lens Included", "Conn: WiFi"]
    elif 'wh-' in name_lower: specs = ["ANC: Best-in-Class Noise Cancellation", "Battery: 30 Hours", "Driver: 40mm", "Conn: Bluetooth 5.3"]
    elif 'savlon' in name_lower: specs = ["Type: Antiseptic Liquid", "Volume: 1000ml", "Action: Kills 99.9% Germs", "Usage: First Aid"]
    elif 'dettol' in name_lower: specs = ["Type: Antiseptic Liquid", "Volume: 500ml", "Action: Disinfectant", "Usage: Multi-Purpose"]
    
    elif any(x in name_lower for x in ['fastrack', 'titan', 'casio', 'fossil', 'watch']):
        specs = ["Type: Analog/Digital", "Water Resistance: 50m", "Warranty: 2 Years", "Material: Stainless Steel/Silicone"]
        if 'smart' in name_lower: specs = ["Display: AMOLED", "Features: SPO2/Heart Rate", "Battery: 7 Days", "GPS: Built-In"]
    
    # Generic
    elif category == 'Fashion': specs = ["Material: Premium Fabric/Leather", "Fit: Regular Fit", "Quality: High", "Wash: Machine Wash"]
    else: specs = ["Quality: Certified", "Warranty: 1 Year"]

    return " | ".join(specs)

def generate_products():
    models = {
        'Electronics': {
            'Apple': ['MacBook Air M1', 'MacBook Air M2', 'MacBook Pro 14', 'iPhone 13', 'iPhone 14', 'iPhone 15 Pro', 'Watch Series 9', 'AirPods Pro 2'],
            'Samsung': ['Galaxy S23 Ultra', 'Galaxy S21 FE', 'Galaxy Z Fold 5', 'Galaxy Book 3', 'Galaxy Watch 6', 'Galaxy Buds 2'],
            'Sony': ['Alpha a7M4 Camera', 'Alpha ZV-E10', 'Bravia 55" 4K TV', 'WH-1000XM5 Headphones', 'PlayStation 5'],
            'Dell': ['XPS 13 Plus', 'Inspiron 15', 'Alienware m15 R7', 'G15 Gaming'],
            'HP': ['Pavilion 15', 'Spectre x360', 'Victus Gaming', 'Deskjet Ink Advantage'],
            'Lenovo': ['ThinkPad X1 Carbon', 'IdeaPad Slim 3', 'Legion 5 Pro', 'Tab M10'],
            'Asus': ['Vivobook 16X', 'TUF Gaming F15', 'ROG Zephyrus G14', 'Zenbook S 13'],
            'Acer': ['Predator Helios', 'Nitro 5', 'Swift Go', 'Aspire 5'],
            'MSI': ['Titan GT77', 'Stealth GS66', 'Katana GF66', 'Modern 14'],
            'Google': ['Pixel 8 Pro', 'Pixel 7a', 'Pixel Watch 2', 'Pixel Buds Pro'],
            'OnePlus': ['OnePlus 11 5G', 'OnePlus Nord CE 3', 'OnePlus Open Fold'],
            'Nothing': ['Phone (2)', 'Phone (1)', 'Nothing Ear (2)'],
            'Realme': ['Realme GT 2 Pro', 'Realme Narzo 60', 'Realme 11 Pro+'],
            'Xiaomi': ['Xiaomi 13 Pro', 'Redmi Note 12', 'Mi Pad 6'],
            'Vivo': ['Vivo X90 Pro', 'Vivo V27', 'Vivo T2x 5G'],
            'Oppo': ['Oppo Reno 10 Pro', 'Oppo F23', 'Oppo Find N3 Flip'],
            'JBL': ['Flip 6 Speaker', 'Boombox 3', 'Live 660NC'],
            'Sennheiser': ['HD 660S2', 'Momentum 4', 'CX Plus'],
            'Panasonic': ['Lumix S5II', 'Lumix GH6', 'Smart TV 4K'],
            'Nikon': ['Z9 Mirrorless', 'Zfc Retro', 'D850 DSLR'],
            'Canon': ['EOS R10 Mirrorless', 'EOS 1500D DSLR', 'Pixma G3000 Printer'],
            'Fastrack': ['Limitless FS1 Smartwatch', 'Fastrack Reflex Beat', 'Stunners Analog Watch'],
            'Titan': ['Titan Neo IV Analog', 'Titan Raga Viva', 'Titan Smart 3'],
            'Casio': ['G-Shock GA-2100', 'Enticer Analog', 'Vintage Digital Watch'],
            'Fossil': ['Gen 6 Smartwatch', 'Grant Chronograph', 'Machine Leather Watch'],
            'Boat': ['Rockerz 450', 'Airdopes 141', 'Xtend Smartwatch', 'Stone 350 Speaker']
        },
        'Fashion': {
            'Nike': ['Air Jordan 1', 'Air Force 1', 'Dri-Fit T-Shirt'],
            'Adidas': ['Ultraboost Light', 'Stan Smith', 'Originals Track Jacket'],
            'Levi\'s': ['501 Original Jeans', 'Sherpa Trucker Jacket', 'Graphic T-Shirt'],
            'H&M': ['Oversized Hoodie', 'Relaxed Fit Jeans', 'Cotton T-Shirt'],
            'Zara': ['Faux Leather Jacket', 'Slim Fit Suit', 'Summer Shirt'],
            'Bata': ['Formal Leather Shoes', 'Casual Loafers', 'Hush Puppies'],
            'Red Tape': ['Formal Oxfords', 'Retro Sneakers', 'Slim Fit Jeans'],
            'Woodland': ['Camel Leather Boots', 'Casual Loafers'],
            'Puma': ['RS-X Sneakers', 'Motorsport T-Shirt']
        },
        'Groceries': {
            'Nestle': ['Maggi Masala Noodles', 'Nescafe Classic', 'KitKat Share Bag'],
            'Britannia': ['Good Day Biscuits', 'Marie Gold', 'Milk Bikis'],
            'ITC': ['Aashirvaad Ghee', 'Sunfeast Dark Fantasy', 'Bingo Mad Angles'],
            'Tata': ['Premium Tea', 'Salt', 'Sampann Pulses'],
            'Dabur': ['Chyawanprash', 'Honey', 'Red Paste'],
            'Savlon': ['Antiseptic Liquid', 'Moisturizing Soap'],
            'Dettol': ['Antiseptic Liquid', 'Liquid Handwash'],
            'Boro Plus': ['Antiseptic Cream', 'Body Lotion'],
            'Colgate': ['Strong Teeth Paste', 'MaxFresh Red Gel'],
            'Amul': ['Salted Butter', 'Taaza Milk', 'Processed Cheese Block'],
            'Maggi': ['2-Minute Masala Noodles']
        }
    }

    products = []
    
    for category, brands in models.items():
        for brand, items in brands.items():
            for item in items:
                if any(x in item for x in [brand, 'iPhone', 'Galaxy', 'MacBook', 'Pixel']):
                    final_name = item
                else:
                    final_name = f"{brand} {item}"
                
                # Generate copies (Increased for 1500+ items)
                for _ in range(18): 
                    price = get_price(final_name, category)
                    price = (price // 100) * 100 + random.choice([0, 99]) # Round off
                    
                    rating = round(random.uniform(4.0, 5.0), 1)
                    specs = get_specs(category, final_name)
                    
                    products.append({
                        'name': final_name,
                        'category': category,
                        'price': price,
                        'rating': rating,
                        'specifications': specs
                    })

    random.shuffle(products)
    
    with open('products.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['product_id', 'product_name', 'category', 'price', 'rating', 'specifications'])
        for i, p in enumerate(products, 1):
            writer.writerow([i, p['name'], p['category'], p['price'], p['rating'], p['specifications']])

    print(f"Generated {len(products)} products with FIXED Pricing (Victus ~65k).")

if __name__ == "__main__":
    generate_products()
