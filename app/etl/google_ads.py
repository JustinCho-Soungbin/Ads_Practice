from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ads import Campaign
from datetime import datetime

MOCK_CAMPAIGNS = [
    {
        "id": "camp_001",
        "name": "Summer Sale - Electronics",
        "ad_spend": 500.00,
        "impressions": 45000,
        "clicks": 1200,
        "google_reported_revenue": 1800.00,
    },
    {
        "id": "camp_002",
        "name": "Back to School - Accessories",
        "ad_spend": 300.00,
        "impressions": 28000,
        "clicks": 750,
        "google_reported_revenue": 950.00,
    },
    {
        "id": "camp_003",
        "name": "Flash Deal - Peripherals",
        "ad_spend": 200.00,
        "impressions": 18000,
        "clicks": 480,
        "google_reported_revenue": 620.00,
    },
]


async def save_campaigns_to_db(session: AsyncSession):
    for c in MOCK_CAMPAIGNS:
        campaign = Campaign(
            id=c["id"],
            name=c["name"],
            ad_spend=c["ad_spend"],
            impressions=c["impressions"],
            clicks=c["clicks"],
            google_reported_revenue=c["google_reported_revenue"],
            created_at=datetime.utcnow(),
        )
        await session.merge(campaign)
    await session.commit()
    print(f"✅ {len(MOCK_CAMPAIGNS)}개 캠페인 저장 완료!")
