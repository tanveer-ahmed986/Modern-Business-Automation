"""
AI Analytics Service for MBAS Premium Features

Handles persistence and retrieval of AI-generated predictions and insights.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from sqlmodel import Session, select, and_

from src.models.ai_analytics import (
    AIAnalytics,
    AIAnalyticsCreate,
    AIAnalyticsRead,
    AnalyticType
)


class AIAnalyticsService:
    """Service for managing AI predictions and analytics."""

    @staticmethod
    def save_prediction(
        session: Session,
        analytic_type: AnalyticType,
        metric_name: str,
        metric_value: float,
        confidence_score: float,
        insight_text: str,
        prediction_horizon: Optional[int] = None,
        entity_id: Optional[int] = None,
        entity_type: Optional[str] = None,
        ttl_days: int = 30
    ) -> AIAnalytics:
        """
        Store AI prediction in database for historical tracking.

        Args:
            session: Database session
            analytic_type: Type of analytics (sales_prediction, inventory_optimization, etc.)
            metric_name: Name of the metric being predicted
            metric_value: Predicted value
            confidence_score: Confidence score (0.0-1.0)
            insight_text: Human-readable insight
            prediction_horizon: Days ahead for predictions
            entity_id: Optional ID of related entity (product, customer, etc.)
            entity_type: Type of entity (product, customer, category)
            ttl_days: Days until prediction expires

        Returns:
            Saved AIAnalytics record
        """
        # Calculate prediction and expiry dates
        now = datetime.utcnow()
        prediction_date = now + timedelta(days=prediction_horizon) if prediction_horizon else now
        expires_at = now + timedelta(days=ttl_days)

        # Create analytics record
        record = AIAnalytics(
            type=analytic_type,
            entity_id=entity_id,
            entity_type=entity_type,
            metric_name=metric_name,
            metric_value=Decimal(str(metric_value)),
            confidence_score=confidence_score,
            insight_text=insight_text,
            prediction_horizon=prediction_horizon,
            prediction_date=prediction_date,
            generated_at=now,
            expires_at=expires_at
        )

        session.add(record)
        session.commit()
        session.refresh(record)

        return record

    @staticmethod
    def get_predictions(
        session: Session,
        analytic_type: Optional[AnalyticType] = None,
        entity_id: Optional[int] = None,
        include_expired: bool = False,
        limit: int = 100
    ) -> List[AIAnalytics]:
        """
        Retrieve AI predictions with optional filtering.

        Args:
            session: Database session
            analytic_type: Filter by analytics type
            entity_id: Filter by entity ID
            include_expired: Include expired predictions
            limit: Maximum number of records to return

        Returns:
            List of AIAnalytics records
        """
        # Build query
        statement = select(AIAnalytics)

        # Apply filters
        filters = []

        if analytic_type:
            filters.append(AIAnalytics.type == analytic_type)

        if entity_id:
            filters.append(AIAnalytics.entity_id == entity_id)

        if not include_expired:
            filters.append(
                and_(
                    AIAnalytics.expires_at.isnot(None),
                    AIAnalytics.expires_at > datetime.utcnow()
                )
            )

        if filters:
            statement = statement.where(and_(*filters))

        # Order by most recent first
        statement = statement.order_by(AIAnalytics.generated_at.desc()).limit(limit)

        # Execute query
        results = session.exec(statement).all()

        return list(results)

    @staticmethod
    def get_latest_prediction(
        session: Session,
        analytic_type: AnalyticType,
        entity_id: Optional[int] = None
    ) -> Optional[AIAnalytics]:
        """
        Get the most recent prediction for a specific type.

        Args:
            session: Database session
            analytic_type: Type of analytics
            entity_id: Optional entity ID filter

        Returns:
            Latest AIAnalytics record or None
        """
        predictions = AIAnalyticsService.get_predictions(
            session=session,
            analytic_type=analytic_type,
            entity_id=entity_id,
            include_expired=False,
            limit=1
        )

        return predictions[0] if predictions else None

    @staticmethod
    def cleanup_expired(session: Session) -> int:
        """
        Delete expired analytics records to keep database clean.

        Args:
            session: Database session

        Returns:
            Number of records deleted
        """
        # Find expired records
        statement = select(AIAnalytics).where(
            and_(
                AIAnalytics.expires_at.isnot(None),
                AIAnalytics.expires_at < datetime.utcnow()
            )
        )

        expired_records = session.exec(statement).all()
        count = len(expired_records)

        # Delete expired records
        for record in expired_records:
            session.delete(record)

        session.commit()

        return count

    @staticmethod
    def get_prediction_history(
        session: Session,
        analytic_type: AnalyticType,
        days: int = 30
    ) -> List[AIAnalytics]:
        """
        Get prediction history for trend analysis.

        Args:
            session: Database session
            analytic_type: Type of analytics
            days: Number of days to look back

        Returns:
            List of historical predictions
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        statement = select(AIAnalytics).where(
            and_(
                AIAnalytics.type == analytic_type,
                AIAnalytics.generated_at >= cutoff_date
            )
        ).order_by(AIAnalytics.generated_at.asc())

        results = session.exec(statement).all()

        return list(results)

    @staticmethod
    def get_accuracy_metrics(
        session: Session,
        analytic_type: AnalyticType,
        days: int = 30
    ) -> dict:
        """
        Calculate accuracy metrics for predictions (if actual values are available).

        Args:
            session: Database session
            analytic_type: Type of analytics
            days: Number of days to analyze

        Returns:
            Dictionary with accuracy metrics
        """
        predictions = AIAnalyticsService.get_prediction_history(
            session=session,
            analytic_type=analytic_type,
            days=days
        )

        if not predictions:
            return {
                "total_predictions": 0,
                "avg_confidence": 0.0,
                "prediction_count_by_horizon": {}
            }

        # Calculate metrics
        total = len(predictions)
        avg_confidence = sum(p.confidence_score or 0.0 for p in predictions) / total

        # Count by prediction horizon
        horizon_counts = {}
        for p in predictions:
            horizon = p.prediction_horizon or 0
            horizon_counts[horizon] = horizon_counts.get(horizon, 0) + 1

        return {
            "total_predictions": total,
            "avg_confidence": round(avg_confidence, 3),
            "prediction_count_by_horizon": horizon_counts,
            "date_range": {
                "start": min(p.generated_at for p in predictions).isoformat(),
                "end": max(p.generated_at for p in predictions).isoformat()
            }
        }


# Export for convenience
__all__ = ["AIAnalyticsService"]
