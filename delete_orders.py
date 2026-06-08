import requests
from dotenv import load_dotenv
import os

load_dotenv()

shop = "justin-ads-audit-test.myshopify.com"
access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
headers = {"X-Shopify-Access-Token": access_token, "Content-Type": "application/json"}

# 기존 주문 ID들
order_ids = [
    6892849266944,
    6892849103104,
    6892849037568,
    6885718655232,
    6885718589696,
    6885718524160,
]

for order_id in order_ids:
    response = requests.delete(
        f"https://{shop}/admin/api/2026-04/orders/{order_id}.json", headers=headers
    )
    if response.status_code == 200:
        print(f"✅ {order_id} 삭제 완료")
    else:
        print(f"❌ {order_id} 에러: {response.json()}")
