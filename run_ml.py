import asyncio
from app.core.database import AsyncSessionLocal
from app.ml.anomaly import detect_roas_anomalies
from app.ml.lstm_autoencoder import detect_lstm_anomalies
from app.ml.ctr_predictor import train_ctr_model


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Isolation Forest ===")
        await detect_roas_anomalies(session)
        print("\n=== LSTM Autoencoder ===")
        await detect_lstm_anomalies(session)
        print("\n=== CTR 예측 (XGBoost) ===")
        await train_ctr_model(session)


asyncio.run(main())
