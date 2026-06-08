# Ads_Practice

# Ad Performance Insight Engine

Google Ads + Shopify 연동 ML 포트폴리오 프로젝트

## Stack

FastAPI · PostgreSQL · Google Ads API · Shopify Admin API · LangGraph · Next.js

## Roadmap

| Phase | 내용                                  | 상태 |
| ----- | ------------------------------------- | ---- |
| 1     | Google Ads API + Shopify API 세팅     | ✅   |
| 2     | ETL 파이프라인 + ROAS 계산            | 🔄   |
| 3     | ML 모델 (anomaly detection, CTR 예측) | 🔲   |
| 4     | Shopify App Store 출시                | 🔲   |

## 핵심 개념

**ROAS (Return on Ad Spend)**

- 공식: `ROAS = Shopify 실제 매출 / 광고비`
- 예: 광고비 $500 썼을 때 매출 $1,000 → ROAS = 2.0
- ROAS 1.0 이하 = 광고비도 못 건짐, 2.0+ = 흑자

**Discrepancy (매출 불일치율)**

- 공식: `Discrepancy = (Google 리포트 매출 - Shopify 실제 매출) / Shopify 실제 매출`
- 예: Google이 $1,800 리포트했는데 Shopify 실제 매출은 $1,200 → Discrepancy = 50%
- 왜 차이나냐?
    - Google은 클릭 후 구매를 모두 자기 기여로 잡음
    - 실제로는 organic, 직접 접속 등 다른 채널 기여도 있음
    - attribution window 차이 (Google 30일 vs 실제 당일)

**CTR (Click Through Rate)**

- 공식: `CTR = 클릭수 / 노출수`
- 예: 노출 10,000번 중 클릭 100번 → CTR = 1%

**Conversion Rate**

- 공식: `CVR = 전환수 / 클릭수`
- 예: 클릭 100번 중 구매 3번 → CVR = 3%

**CPC (Cost Per Click) - 클릭당 비용**

- 공식: `CPC = 광고비 / 클릭수`
- 예: 광고비 $500, 클릭 1,000번 → CPC = $0.50
- 낮을수록 효율적인 광고

**CPM (Cost Per Mille) - 1,000 노출당 비용**

- 공식: `CPM = (광고비 / 노출수) × 1,000`
- 예: 광고비 $500, 노출 100,000번 → CPM = $5.00
- 브랜드 인지도 캠페인에서 주로 사용

**CPA (Cost Per Acquisition) - 전환 1건당 비용**

- 공식: `CPA = 광고비 / 전환수`
- 예: 광고비 $500, 구매 25건 → CPA = $20.00
- 낮을수록 광고 효율 좋음, ROAS랑 같이 봐야 함

## ML 모델

**Isolation Forest (이상 감지)**

- 비지도 학습 기반 이상 감지 알고리즘
- 원리: 이상한 데이터는 decision tree에서 빨리 고립됨
- 입력: ROAS, Discrepancy, Ad Spend, Shopify Revenue
- 출력: 정상(-1 아님) / 이상(-1) + anomaly score
- Score가 0에 가까울수록 정상, -1에 가까울수록 이상

**LSTM Autoencoder (시계열 이상 감지)**

- 시계열 데이터의 정상 패턴을 학습 후 재구성 오차로 이상 탐지
- 원리: 정상 패턴은 재구성 잘 됨 → 오차 작음 / 이상 패턴은 재구성 못 함 → 오차 큼
- 입력: 캠페인별 일별 ROAS 시계열 (7일 윈도우 슬라이딩)
- 출력: 구간별 재구성 오차 + 임계값 초과 시 이상 구간 표시
- 실사용: 광고 ROAS 급락 구간 자동 감지

## 메모

- Shopify: 더미 주문으로 테스트
- Google Ads: mock data로 테스트 후 Test Account
