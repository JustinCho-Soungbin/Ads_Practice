import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ads import DailyMetric, Campaign


async def train_ctr_model(session: AsyncSession):
    # 데이터 가져오기
    metrics = (
        (await session.execute(select(DailyMetric).order_by(DailyMetric.date)))
        .scalars()
        .all()
    )

    if len(metrics) < 20:
        print("⚠️ 데이터 부족")
        return

    # Feature Engineering
    df = pd.DataFrame(
        [
            {
                "campaign_id": m.campaign_id,
                "ad_spend": m.ad_spend,
                "impressions": m.impressions,
                "clicks": m.clicks,
                "revenue": m.revenue,
                "roas": m.roas,
                "ctr": m.clicks / m.impressions if m.impressions > 0 else 0,
                "day_of_week": m.date.weekday(),
                "day_of_month": m.date.day,
            }
            for m in metrics
        ]
    )

    # campaign_id → 숫자로 인코딩
    df["campaign_encoded"] = df["campaign_id"].map(
        {"camp_001": 0, "camp_002": 1, "camp_003": 2}
    )

    # Feature / Target 분리
    # impressions 빼고
    features = [
        "ad_spend",
        "revenue",
        "roas",
        "day_of_week",
        "day_of_month",
        "campaign_encoded",
    ]
    X = df[features]
    y = df["ctr"]

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # XGBoost 학습
    model = GradientBoostingRegressor(
        n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42
    )
    model.fit(X_train, y_train)

    # 평가
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    print("\n📊 CTR 예측 모델 (XGBoost)")
    print(f"   RMSE: {rmse:.4f}")
    print(f"   R²: {r2:.4f}")

    # Feature Importance
    importance = pd.Series(model.feature_importances_, index=features).sort_values(
        ascending=False
    )
    print("\n   Feature Importance:")
    for feat, score in importance.items():
        print(f"   {feat}: {score:.4f}")

    return model
