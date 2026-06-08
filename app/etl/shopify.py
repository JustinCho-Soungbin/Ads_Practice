import httpx
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ads import ShopifyOrder
from datetime import datetime

load_dotenv()

SHOP = "justin-ads-audit-test.myshopify.com"
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")


async def fetch_shopify_orders():
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{SHOP}/admin/api/2026-04/orders.json?status=any&limit=250",
            headers=headers,
        )
        return response.json().get("orders", [])


async def save_orders_to_db(session: AsyncSession):
    orders = await fetch_shopify_orders()
    for o in orders:
        order = ShopifyOrder(
            id=str(o["id"]),
            order_number=o["order_number"],
            total_price=float(o["total_price"]),
            campaign_id=None,
            created_at=datetime.fromisoformat(o["created_at"]).replace(tzinfo=None),
        )
        await session.merge(order)
    await session.commit()
    print(f"✅ {len(orders)}개 주문 저장 완료!")
