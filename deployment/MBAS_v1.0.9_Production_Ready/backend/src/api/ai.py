from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..core.db import get_session
from ..core.auth import get_current_user
from ..core.features import check_feature
from ..models.core import User, UserRole
from ..models.sales import Sale
from ..models.ai_analytics import AnalyticType
from ..ai.forecasting import SalesForecaster
from ..ai.llm import llm_service
from ..services.ai_service import AIAnalyticsService

router = APIRouter(prefix="/ai", tags=["ai"])

def get_admin(current_user: User = Depends(get_current_user)):
    """Ensures only admins can access AI features."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access AI features."
        )
    return current_user

@router.get("/predict")
def get_sales_prediction(
    n_days: int = Query(30, ge=1, le=365),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("ai_assistant"))
) -> List[Dict[str, Any]]:
    """
    Predicts sales for the next N days based on historical data.
    Requires 'ai_assistant' premium feature.
    """
    # Fetch historical sales data
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=365) # Use last year's data for training
    
    sales_data_query = (
        select(
            func.date(Sale.created_at).label("date"),
            func.sum(Sale.grand_total).label("revenue")
        )
        .where(Sale.created_at.between(start_date, end_date), Sale.status == "completed")
        .group_by(func.date(Sale.created_at))
        .order_by(func.date(Sale.created_at))
    )
    
    historical_sales = session.exec(sales_data_query).all()
    
    # Convert to format expected by forecaster
    formatted_sales = [{"date": str(s[0]), "revenue": float(s[1])} for s in historical_sales]
    
    forecaster = SalesForecaster()
    if not forecaster.train(formatted_sales):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough historical sales data to train the forecasting model."
        )

    predictions = forecaster.predict_next_n_days(n_days)

    # Save prediction to database for historical tracking
    if predictions:
        total_predicted = sum(p["predicted_revenue"] for p in predictions)
        avg_confidence = sum(p.get("confidence", 0.75) for p in predictions) / len(predictions)

        AIAnalyticsService.save_prediction(
            session=session,
            analytic_type=AnalyticType.SALES_PREDICTION,
            metric_name="total_predicted_revenue",
            metric_value=total_predicted,
            confidence_score=avg_confidence,
            insight_text=f"Predicted ${total_predicted:,.2f} revenue over next {n_days} days",
            prediction_horizon=n_days,
            ttl_days=n_days + 7  # Keep prediction for a week after horizon
        )

    return predictions

@router.post("/query")
def natural_language_query(
    prompt: str,
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("ai_assistant"))
) -> Dict[str, str]:
    """
    Processes a natural language query using the LLM.
    Requires 'ai_assistant' premium feature.
    """
    response = llm_service.query(prompt)
    return {"response": response}


@router.get("/predictions/history")
def get_prediction_history(
    analytic_type: AnalyticType = Query(AnalyticType.SALES_PREDICTION),
    days: int = Query(30, ge=1, le=365),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("ai_assistant"))
) -> List[Dict[str, Any]]:
    """
    Retrieve historical AI predictions for trend analysis.
    Requires 'ai_assistant' premium feature.
    """
    predictions = AIAnalyticsService.get_prediction_history(
        session=session,
        analytic_type=analytic_type,
        days=days
    )

    return [
        {
            "id": p.id,
            "metric_name": p.metric_name,
            "metric_value": float(p.metric_value),
            "confidence_score": p.confidence_score,
            "insight_text": p.insight_text,
            "prediction_horizon": p.prediction_horizon,
            "generated_at": p.generated_at.isoformat(),
            "prediction_date": p.prediction_date.isoformat() if p.prediction_date else None
        }
        for p in predictions
    ]


@router.get("/predictions/accuracy")
def get_prediction_accuracy(
    analytic_type: AnalyticType = Query(AnalyticType.SALES_PREDICTION),
    days: int = Query(30, ge=1, le=365),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("ai_assistant"))
) -> Dict[str, Any]:
    """
    Get accuracy metrics for AI predictions.
    Requires 'ai_assistant' premium feature.
    """
    metrics = AIAnalyticsService.get_accuracy_metrics(
        session=session,
        analytic_type=analytic_type,
        days=days
    )

    return metrics


@router.delete("/predictions/cleanup")
def cleanup_expired_predictions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin),
    has_feature: bool = Depends(check_feature("ai_assistant"))
) -> Dict[str, Any]:
    """
    Clean up expired prediction records.
    Requires 'ai_assistant' premium feature.
    """
    count = AIAnalyticsService.cleanup_expired(session=session)

    return {
        "deleted_count": count,
        "message": f"Cleaned up {count} expired prediction(s)"
    }
