from typing import List
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta
import numpy as np

class SalesForecaster:
    def __init__(self):
        self.model = LinearRegression()
        self.trained = False

    def train(self, sales_data: List[dict]):
        """
        Trains the forecasting model using historical sales data.
        sales_data: List of dictionaries, each with 'date' and 'revenue' (or similar).
        """
        if not sales_data:
            self.trained = False
            return False

        # Convert to DataFrame
        df = pd.DataFrame(sales_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Aggregate daily sales
        daily_sales = df['revenue'].resample('D').sum().fillna(0)
        
        # Create features: day of week, day of month, month, year, etc.
        # For simplicity, we'll use a sequential day number as the primary feature.
        # In a real scenario, more complex feature engineering would be needed.
        features = np.array([(d - daily_sales.index.min()).days for d in daily_sales.index]).reshape(-1, 1)
        targets = daily_sales.values
        
        if len(features) < 2: # Need at least 2 data points to train a linear model
            self.trained = False
            return False

        self.model.fit(features, targets)
        self.trained = True
        return True

    def predict_next_n_days(self, n_days: int = 30) -> List[dict]:
        """
        Predicts sales for the next N days.
        Returns a list of dictionaries with 'date' and 'predicted_revenue'.
        """
        if not self.trained:
            return []

        # Get the last date from training data
        last_training_date = pd.to_datetime(self.model.feature_names_in_[0] if hasattr(self.model, 'feature_names_in_') else '1970-01-01') # Fallback
        
        # Create future dates and their corresponding features
        future_dates = [last_training_date + timedelta(days=i) for i in range(1, n_days + 1)]
        future_features = np.array([(d - last_training_date).days + 1 for d in future_dates]).reshape(-1, 1)
        
        predictions = self.model.predict(future_features)
        
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "date": future_dates[i].isoformat().split('T')[0],
                "predicted_revenue": max(0, float(pred)) # Revenue cannot be negative
            })
        return results

if __name__ == "__main__":
    # Example Usage
    sample_sales = [
        {"date": "2023-01-01", "revenue": 100},
        {"date": "2023-01-02", "revenue": 120},
        {"date": "2023-01-03", "revenue": 110},
        {"date": "2023-01-04", "revenue": 130},
        {"date": "2023-01-05", "revenue": 150},
        {"date": "2023-01-06", "revenue": 140},
        {"date": "2023-01-07", "revenue": 160},
        {"date": "2023-01-08", "revenue": 170},
        {"date": "2023-01-09", "revenue": 155},
        {"date": "2023-01-10", "revenue": 180},
    ]

    forecaster = SalesForecaster()
    if forecaster.train(sample_sales):
        print("Model trained successfully.")
        predictions = forecaster.predict_next_n_days(7)
        print("Next 7 days sales predictions:")
        for p in predictions:
            print(f"Date: {p['date']}, Predicted Revenue: {p['predicted_revenue']:.2f}")
    else:
        print("Not enough data to train the model.")
