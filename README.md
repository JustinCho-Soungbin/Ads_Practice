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

## 메모

- Shopify: 더미 주문으로 테스트
- Google Ads: mock data로 테스트 후 Test Account
