import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ads import RoasReport, Campaign


async def detect_roas_anomalies(session: AsyncSession):
    # DB에서 ROAS 데이터 가져오기
    reports = (
        await session.execute(
            select(RoasReport, Campaign.name).join(
                Campaign, RoasReport.campaign_id == Campaign.id
            )
        )
    ).all()

    if len(reports) < 2:
        print("⚠️ 데이터 부족 — 최소 2개 이상 필요")
        return

    # DataFrame 만들기
    data = [
        {
            "campaign_name": r.name,
            "roas": r.RoasReport.roas,
            "discrepancy": r.RoasReport.discrepancy,
            "ad_spend": r.RoasReport.ad_spend,
            "shopify_revenue": r.RoasReport.shopify_revenue,
        }
        for r in reports
    ]

    df = pd.DataFrame(data)
    features = df[["roas", "discrepancy", "ad_spend", "shopify_revenue"]]

    # Isolation Forest
    model = IsolationForest(contamination=0.3, random_state=42)
    df["anomaly"] = model.fit_predict(features)
    df["anomaly_score"] = model.score_samples(features)

    print("\n📊 Anomaly Detection 결과:")
    print("-" * 50)
    for _, row in df.iterrows():
        status = "🚨 이상" if row["anomaly"] == -1 else "✅ 정상"
        print(f"{status} | {row['campaign_name']}")
        print(
            f"      ROAS: {row['roas']} | Discrepancy: {row['discrepancy']*100:.1f}% | Score: {row['anomaly_score']:.4f}"
        )

    return df
