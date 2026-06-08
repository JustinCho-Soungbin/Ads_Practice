from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from app.models.ads import Campaign, ShopifyOrder, RoasReport
from datetime import datetime


async def calculate_roas(session: AsyncSession):
    campaigns = (await session.execute(select(Campaign))).scalars().all()

    for campaign in campaigns:
        # Shopify 실제 매출 (campaign_id 없으니까 균등 배분)
        total_shopify = (
            await session.execute(select(func.sum(ShopifyOrder.total_price)))
        ).scalar() or 0.0

        # 캠페인 수로 나눠서 배분 (mock이라 attribution 없음)
        shopify_revenue = round(total_shopify / len(campaigns), 2)

        roas = round(shopify_revenue / campaign.ad_spend, 4) if campaign.ad_spend else 0
        discrepancy = (
            round(
                (campaign.google_reported_revenue - shopify_revenue) / shopify_revenue,
                4,
            )
            if shopify_revenue
            else 0
        )
        ctr = (
            round(campaign.clicks / campaign.impressions, 4)
            if campaign.impressions
            else 0
        )
        cpc = round(campaign.ad_spend / campaign.clicks, 2) if campaign.clicks else 0

        report = RoasReport(
            campaign_id=campaign.id,
            shopify_revenue=shopify_revenue,
            google_reported_revenue=campaign.google_reported_revenue,
            ad_spend=campaign.ad_spend,
            roas=roas,
            discrepancy=discrepancy,
            calculated_at=datetime.utcnow(),
        )
        stmt = (
            insert(RoasReport)
            .values(
                campaign_id=campaign.id,
                shopify_revenue=shopify_revenue,
                google_reported_revenue=campaign.google_reported_revenue,
                ad_spend=campaign.ad_spend,
                roas=roas,
                discrepancy=discrepancy,
                calculated_at=datetime.utcnow(),
            )
            .on_conflict_do_update(
                constraint="uq_roas_campaign",
                set_={
                    "shopify_revenue": shopify_revenue,
                    "google_reported_revenue": campaign.google_reported_revenue,
                    "roas": roas,
                    "discrepancy": discrepancy,
                    "calculated_at": datetime.utcnow(),
                },
            )
        )
        await session.execute(stmt)
        print(f"📊 {campaign.name}")
        print(f"   ROAS: {roas} | Discrepancy: {discrepancy*100:.1f}%")
        print(f"   CTR: {ctr*100:.2f}% | CPC: ${cpc}")

    await session.commit()
    print("✅ ROAS 계산 완료!")
