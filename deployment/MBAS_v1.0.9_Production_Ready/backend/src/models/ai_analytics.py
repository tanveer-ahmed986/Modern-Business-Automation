from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from decimal import Decimal
from enum import Enum

class AnalyticType(str, Enum):
    """Type of AI-generated analytics."""
    SALES_PREDICTION = "sales_prediction"
    INVENTORY_OPTIMIZATION = "inventory_optimization"
    PROFIT_ANALYSIS = "profit_analysis"
    CUSTOMER_INSIGHT = "customer_insight"
    PRODUCT_RECOMMENDATION = "product_recommendation"
    SLOW_MOVING_ALERT = "slow_moving_alert"
    REORDER_ALERT = "reorder_alert"

class AIAnalyticsBase(SQLModel):
    """Premium feature: Store AI-generated predictions and insights."""
    type: AnalyticType
    entity_id: Optional[int] = Field(default=None)  # Links to Product, Customer, etc.
    entity_type: Optional[str] = Field(default=None)  # "product", "customer", "category"
    metric_name: str  # e.g., "next_month_revenue", "reorder_quantity", "profit_margin"
    metric_value: Decimal = Field(default=0.0)
    confidence_score: Optional[float] = Field(default=None)  # 0.0-1.0 confidence
    insight_text: Optional[str] = Field(default=None)  # Human-readable insight
    prediction_horizon: Optional[int] = Field(default=None)  # Days ahead for predictions

class AIAnalytics(AIAnalyticsBase, table=True):
    __tablename__ = "ai_analytics"
    id: Optional[int] = Field(default=None, primary_key=True)
    prediction_date: datetime = Field(default_factory=datetime.utcnow, index=True)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)  # When prediction becomes stale

class AIAnalyticsCreate(AIAnalyticsBase):
    pass

class AIAnalyticsRead(AIAnalyticsBase):
    id: int
    prediction_date: datetime
    generated_at: datetime
    expires_at: Optional[datetime]
