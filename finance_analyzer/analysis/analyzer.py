import pandas as pd
from typing import Dict

class FinancialAnalyzer:
    """Handles basic financial analysis for MVP."""
    
    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> Dict[str, float]:
        """Calculate core financial metrics."""
        return {
            'ROE': df['net_income'] / df['equity'],
            'revenue_growth': df['revenue'].pct_change(),
            'operating_margin': df['operating_income'] / df['revenue']
        }
    
    @staticmethod
    def analyze_trend(df: pd.DataFrame, metric: str) -> str:
        """Analyze trend for a specific metric."""
        if df[metric].iloc[-1] > df[metric].iloc[0]:
            return f"{metric} 呈現上升趨勢，從{df[metric].iloc[0]:.1%}提升至{df[metric].iloc[-1]:.1%}"
        elif df[metric].iloc[-1] < df[metric].iloc[0]:
            return f"{metric} 呈現下降趨勢，從{df[metric].iloc[0]:.1%}降至{df[metric].iloc[-1]:.1%}"
        else:
            return f"{metric} 維持穩定，約在{df[metric].iloc[0]:.1%}左右" 