import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ads import DailyMetric, Campaign


class LSTMAutoencoder(nn.Module):
    def __init__(self, input_size=1, hidden_size=32, num_layers=2):
        super().__init__()
        self.encoder = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.decoder = nn.LSTM(hidden_size, input_size, num_layers, batch_first=True)

    def forward(self, x):
        _, (hidden, cell) = self.encoder(x)
        # hidden을 decoder input으로
        decoder_input = hidden[-1].unsqueeze(1).repeat(1, x.size(1), 1)
        output, _ = self.decoder(decoder_input)
        return output


async def detect_lstm_anomalies(session: AsyncSession, threshold: float = 0.5):
    campaigns = (await session.execute(select(Campaign))).scalars().all()

    for campaign in campaigns:
        # 시계열 데이터 가져오기
        metrics = (
            (
                await session.execute(
                    select(DailyMetric)
                    .where(DailyMetric.campaign_id == campaign.id)
                    .order_by(DailyMetric.date)
                )
            )
            .scalars()
            .all()
        )

        if len(metrics) < 10:
            print(f"⚠️ {campaign.name} 데이터 부족")
            continue

        # ROAS 시계열 추출
        roas_values = np.array([m.roas for m in metrics], dtype=np.float32)

        # 정규화
        mean, std = roas_values.mean(), roas_values.std()
        normalized = (roas_values - mean) / (std + 1e-8)

        # 윈도우 슬라이딩 (7일 단위)
        window = 7
        sequences = []
        for i in range(len(normalized) - window + 1):
            sequences.append(normalized[i : i + window])

        X = torch.tensor(sequences, dtype=torch.float32).unsqueeze(-1)

        # 모델 학습
        model = LSTMAutoencoder()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        criterion = nn.MSELoss()

        model.train()
        for epoch in range(50):
            optimizer.zero_grad()
            output = model(X)
            loss = criterion(output, X)
            loss.backward()
            optimizer.step()

        # 재구성 오차 계산
        model.eval()
        with torch.no_grad():
            output = model(X)
            errors = ((output - X) ** 2).mean(dim=(1, 2)).numpy()

        # 이상 탐지
        anomaly_threshold = errors.mean() + threshold * errors.std()
        anomalies = np.where(errors > anomaly_threshold)[0]

        print(f"\n📊 LSTM Anomaly Detection - {campaign.name}")
        print(f"   평균 재구성 오차: {errors.mean():.4f}")
        print(f"   임계값: {anomaly_threshold:.4f}")
        if len(anomalies) > 0:
            print(f"   🚨 이상 구간 (window 시작일 기준):")
            for idx in anomalies:
                print(f"      Day {idx+1}~{idx+window}: error={errors[idx]:.4f}")
