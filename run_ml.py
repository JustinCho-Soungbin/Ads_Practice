import asyncio
from app.core.database import AsyncSessionLocal
from app.ml.anomaly import detect_roas_anomalies
from app.ml.lstm_autoencoder import detect_lstm_anomalies


async def main():
    async with AsyncSessionLocal() as session:
        print("=== Isolation Forest ===")
        await detect_roas_anomalies(session)
        print("\n=== LSTM Autoencoder ===")
        await detect_lstm_anomalies(session)


asyncio.run(main())
