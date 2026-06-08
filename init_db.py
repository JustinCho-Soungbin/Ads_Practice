from dotenv import load_dotenv

load_dotenv()  # 맨 위에 추가

import asyncio
from app.core.database import engine, Base
from app.models.ads import Campaign, ShopifyOrder, RoasReport


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created!")


asyncio.run(init())
