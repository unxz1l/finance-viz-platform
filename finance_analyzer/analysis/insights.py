"""
Financial insights generation module for MVP.
This module provides basic insights generation for core financial metrics.
"""

from typing import List, Dict
import pandas as pd


class InsightGenerator:
    """Class for generating basic financial insights."""
    
    @staticmethod
    def generate_metric_insight(df: pd.DataFrame, metric: str) -> str:
        """
        Generate simple insight for a specific metric.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing financial data
        metric : str
            Metric name to analyze
            
        Returns
        -------
        str
            Simple insight about the metric trend
        """
        if metric not in df.columns:
            return f"無法分析 {metric}，資料不存在"
            
        current_value = df[metric].iloc[-1]
        previous_value = df[metric].iloc[0]
        change = current_value - previous_value
        
        if change > 0:
            return f"{metric} 呈現上升趨勢，從{previous_value:.1%}提升至{current_value:.1%}"
        elif change < 0:
            return f"{metric} 呈現下降趨勢，從{previous_value:.1%}降至{current_value:.1%}"
        else:
            return f"{metric} 維持穩定，約在{current_value:.1%}左右"
    
    @staticmethod
    def generate_core_insights(df: pd.DataFrame) -> Dict[str, str]:
        """
        Generate insights for core financial metrics.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing financial data
            
        Returns
        -------
        Dict[str, str]
            Dictionary of insights for each core metric
        """
        core_metrics = ['ROE', 'revenue_growth', 'operating_margin']
        insights = {}
        
        for metric in core_metrics:
            insights[metric] = InsightGenerator.generate_metric_insight(df, metric)
            
        return insights