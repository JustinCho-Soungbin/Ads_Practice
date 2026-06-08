import asyncio
from app.core.database import AsyncSessionLocal
from app.etl.shopify import save_orders_to_db
from app.etl.google_ads import save_campaigns_to_db
from app.etl.roas import calculate_roas


async def main():
    async with AsyncSessionLocal() as session:
        await save_campaigns_to_db(session)
        await save_orders_to_db(session)
        await calculate_roas(session)


asyncio.run(main())
