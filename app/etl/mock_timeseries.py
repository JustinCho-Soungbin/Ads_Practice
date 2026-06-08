import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ads import DailyMetric, Campaign


async def generate_timeseries(session: AsyncSession, days: int = 60):
    campaigns = (await session.execute(select(Campaign))).scalars().all()

    for campaign in campaigns:
        base_roas = {"camp_001": 0.85, "camp_002": 1.40, "camp_003": 2.10}
        base = base_roas.get(campaign.id, 1.5)

        for i in range(days):
            date = datetime.utcnow() - timedelta(days=days - i)

            # 정상 구간 + 이상 구간 만들기
            if 20 <= i <= 25:  # 이상 구간
                noise = np.random.normal(0, 0.8)
            else:  # 정상 구간
                noise = np.random.normal(0, 0.15)

            roas = max(0.1, base + noise)
            ad_spend = campaign.ad_spend / days
            revenue = ad_spend * roas
            clicks = int(campaign.clicks / days * np.random.uniform(0.8, 1.2))
            impressions = int(campaign.impressions / days * np.random.uniform(0.8, 1.2))

            metric = DailyMetric(
                campaign_id=campaign.id,
                date=date,
                ad_spend=round(ad_spend, 2),
                impressions=impressions,
                clicks=clicks,
                revenue=round(revenue, 2),
                roas=round(roas, 4),
            )
            session.add(metric)

        print(f"✅ {campaign.name} - {days}일 데이터 생성 완료")

    await session.commit()
