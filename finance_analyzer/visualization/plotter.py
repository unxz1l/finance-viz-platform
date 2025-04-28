"""
Basic financial data visualization module.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class FinancialPlotter:
    """Handles basic financial data visualization."""
    
    @staticmethod
    def plot_metric_trend(df: pd.DataFrame, metric: str) -> go.Figure:
        """Plot trend for a specific metric."""
        fig = px.line(
            df,
            x='year',
            y=metric,
            title=f"{metric} 趨勢",
            markers=True
        )
        fig.update_layout(
            xaxis_title="年度",
            yaxis_title=metric,
            hovermode="x unified"
        )
        return fig
    
    @staticmethod
    def format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Format dataframe for display."""
        return df.style.format({
            'ROE': '{:.1%}',
            'Operating_Margin': '{:.1%}',
            'Debt_Ratio': '{:.1%}',
            'Revenue_Growth': '{:.1%}'
        }) 