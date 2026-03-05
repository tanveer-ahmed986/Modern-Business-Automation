from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..core.db import get_session
from ..core.auth import get_current_user
from ..core.features import check_feature
from ..models.core import User, UserRole
from ..models.sales import Sale
from ..ai.forecasting import SalesForecaster
from ..ai.llm import llm_service

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
