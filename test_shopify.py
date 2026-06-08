import requests
from dotenv import load_dotenv
import os

load_dotenv()

shop = "justin-ads-audit-test.myshopify.com"
access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

headers = {"X-Shopify-Access-Token": access_token}

response = requests.get(
    f"https://{shop}/admin/api/2026-04/orders.json?status=any&limit=250",
    headers=headers,
)
print(response.status_code)
print(response.json())
