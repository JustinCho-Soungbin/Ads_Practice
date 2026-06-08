import requests
from dotenv import load_dotenv
import os
import random
import time

load_dotenv()

shop = "justin-ads-audit-test.myshopify.com"
access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
headers = {"X-Shopify-Access-Token": access_token, "Content-Type": "application/json"}

products = [
    {"title": "Wireless Earbuds", "price": "49.99"},
    {"title": "Phone Case", "price": "19.99"},
    {"title": "USB-C Cable", "price": "12.99"},
    {"title": "Laptop Stand", "price": "89.99"},
    {"title": "Mechanical Keyboard", "price": "129.99"},
    {"title": "Webcam HD", "price": "79.99"},
    {"title": "Mouse Pad XL", "price": "24.99"},
    {"title": "Screen Cleaner", "price": "9.99"},
]

for i in range(20):
    product = random.choice(products)
    qty = random.randint(1, 3)
    total = round(float(product["price"]) * qty, 2)
    order = {
        "order": {
            "line_items": [
                {"title": product["title"], "price": product["price"], "quantity": qty}
            ],
            "financial_status": "paid",
            "total_price": str(total),
            "email": f"customer{i+1}@example.com",
        }
    }
    response = requests.post(
        f"https://{shop}/admin/api/2026-04/orders.json", headers=headers, json=order
    )
    data = response.json()
    if "order" in data:
        print(
            f"✅ #{data['order']['order_number']} - {product['title']} x{qty} = ${total}"
        )
    else:
        print(f"❌ 에러: {data}")
    time.sleep(2)
