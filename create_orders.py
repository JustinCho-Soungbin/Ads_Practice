import 
from dotenv import load_dotenv
import os
load_dotenv()

shop = "justin-ads-audit-test.myshopify.com"
access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
headers = {
    "X-Shopify-Access-Token": access_token,
    "Content-Type": "application/json"
}

# 더미 주문 3개 생성
for i in range(3):
    order = {
        "order": {
            "line_items": [{"variant_id": None, "title": f"Test Product {i+1}", "price": "29.99", "quantity": 1}],
            "financial_status": "paid",
            "total_price": "29.99",
            "email": f"test{i+1}@example.com"
        }
    }
    response = requests.post(
        f"https://{shop}/admin/api/2026-04/orders.json",
        headers=headers,
        json=order
    )
    data = response.json()
    if "order" in data:
        print(f"✅ 주문 #{data['order']['order_number']} 생성 완료")
    else:
        print(f"❌ 에러: {data}")
