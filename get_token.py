import requests
from dotenv import load_dotenv
import os

load_dotenv()

shop = "justin-ads-audit-test.myshopify.com"
client_id = os.getenv("SHOPIFY_CLIENT_ID")
client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")

url = f"https://{shop}/admin/oauth/access_token"
payload = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials",
}

response = requests.post(url, json=payload)
print(response.json())
