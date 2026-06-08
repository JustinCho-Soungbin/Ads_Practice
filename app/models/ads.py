from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime


class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(String, primary_key=True)
    name = Column(String)
    ad_spend = Column(Float, default=0.0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    google_reported_revenue = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ShopifyOrder(Base):
    __tablename__ = "shopify_orders"
    id = Column(String, primary_key=True)
    order_number = Column(Integer)
    total_price = Column(Float)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=True)
    created_at = Column(DateTime)


class RoasReport(Base):
    __tablename__ = "roas_reports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    shopify_revenue = Column(Float)
    google_reported_revenue = Column(Float)
    ad_spend = Column(Float)
    roas = Column(Float)  # shopify_revenue / ad_spend
    discrepancy = Column(Float)  # (google - shopify) / shopify
    calculated_at = Column(DateTime, default=datetime.datetime.utcnow)
