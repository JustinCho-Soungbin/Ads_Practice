import asyncio
from app.core.database import AsyncSessionLocal
from app.etl.shopify import save_orders_to_db
from app.etl.google_ads import save_campaigns_to_db
from app.etl.roas import calculate_roas
from app.etl.mock_timeseries import generate_timeseries


async def main():
    async with AsyncSessionLocal() as session:
        await save_campaigns_to_db(session)
        await save_orders_to_db(session)
        await calculate_roas(session)
        await generate_timeseries(session)


asyncio.run(main())
