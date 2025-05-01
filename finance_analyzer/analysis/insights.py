"""
Financial insights generation module.

This module provides functions to generate meaningful insights and analysis
from financial indicators and metrics.
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


class FinancialInsights:
    """Class for generating financial insights and analysis."""
    
    @staticmethod
    def analyze_trend(series: pd.Series, metric_name: str) -> str:
        """
        Analyze the trend of a financial metric.
        
        Parameters
        ----------
        series : pd.Series
            Time series data of the metric
        metric_name : str
            Name of the metric being analyzed
            
        Returns
        -------
        str
            Insight about the metric's trend
        """
        if series.empty:
            return f"無法分析 {metric_name}，資料不存在"
            
        current_value = series.iloc[-1]
        previous_value = series.iloc[0]
        change = current_value - previous_value
        
        if change > 0:
            return f"{metric_name} 呈現上升趨勢，從{previous_value:.1f}%提升至{current_value:.1f}%"
        elif change < 0:
            return f"{metric_name} 呈現下降趨勢，從{previous_value:.1f}%降至{current_value:.1f}%"
        else:
            return f"{metric_name} 維持穩定，約在{current_value:.1f}%左右"
    
    @staticmethod
    def analyze_volatility(series: pd.Series, metric_name: str) -> str:
        """
        Analyze the volatility of a financial metric.
        
        Parameters
        ----------
        series : pd.Series
            Time series data of the metric
        metric_name : str
            Name of the metric being analyzed
            
        Returns
        -------
        str
            Insight about the metric's volatility
        """
        if series.empty:
            return f"無法分析 {metric_name} 的波動性，資料不存在"
            
        std_dev = series.std()
        mean = series.mean()
        cv = (std_dev / mean) * 100 if mean != 0 else float('inf')
        
        if cv < 10:
            return f"{metric_name} 波動性低，變異係數為{cv:.1f}%"
        elif cv < 30:
            return f"{metric_name} 波動性中等，變異係數為{cv:.1f}%"
        else:
            return f"{metric_name} 波動性高，變異係數為{cv:.1f}%"
    
    @staticmethod
    def analyze_relative_performance(series: pd.Series, 
                                   benchmark: float,
                                   metric_name: str) -> str:
        """
        Analyze the performance relative to a benchmark.
        
        Parameters
        ----------
        series : pd.Series
            Time series data of the metric
        benchmark : float
            Benchmark value to compare against
        metric_name : str
            Name of the metric being analyzed
            
        Returns
        -------
        str
            Insight about the metric's relative performance
        """
        if series.empty:
            return f"無法分析 {metric_name} 的相對表現，資料不存在"
            
        current_value = series.iloc[-1]
        difference = current_value - benchmark
        
        if difference > 0:
            return f"{metric_name} 表現優於基準，高出{abs(difference):.1f}%"
        elif difference < 0:
            return f"{metric_name} 表現低於基準，低出{abs(difference):.1f}%"
        else:
            return f"{metric_name} 表現與基準持平"
    
    @staticmethod
    def generate_comprehensive_insights(ratios: Dict[str, pd.Series]) -> Dict[str, List[str]]:
        """
        Generate comprehensive insights for all financial ratios.
        
        Parameters
        ----------
        ratios : Dict[str, pd.Series]
            Dictionary of financial ratios and their time series data
            
        Returns
        -------
        Dict[str, List[str]]
            Dictionary of insights for each ratio
        """
        insights = {}
        
        # Define industry benchmarks (these should be customized based on actual data)
        benchmarks = {
            "ROE": 15.0,  # 15% is often considered a good ROE
            "ROA": 5.0,   # 5% is often considered a good ROA
            "Debt Ratio": 50.0,  # 50% is often considered a balanced debt ratio
            "Profit Margin": 10.0,  # 10% is often considered a good profit margin
            "Revenue Growth": 5.0   # 5% is often considered healthy growth
        }
        
        for metric, series in ratios.items():
            metric_insights = []
            
            # Analyze trend
            trend_insight = FinancialInsights.analyze_trend(series, metric)
            metric_insights.append(trend_insight)
            
            # Analyze volatility
            volatility_insight = FinancialInsights.analyze_volatility(series, metric)
            metric_insights.append(volatility_insight)
            
            # Analyze relative performance if benchmark exists
            if metric in benchmarks:
                relative_insight = FinancialInsights.analyze_relative_performance(
                    series, benchmarks[metric], metric
                )
                metric_insights.append(relative_insight)
            
            insights[metric] = metric_insights
        
        return insights

    @staticmethod
    def assess_risk(df: pd.DataFrame) -> Dict[str, str]:
        """
        Assess investment risk based on key financial metrics.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing financial metrics
            
        Returns
        -------
        Dict[str, str]
            Dictionary of risk assessments for each metric
        """
        risk_assessment = {}
        
        # ROE assessment
        if df['ROE'].iloc[-1] > 15:
            risk_assessment['ROE'] = "ROE表現良好"
        else:
            risk_assessment['ROE'] = "ROE表現需注意"
            
        # Revenue Growth assessment
        if df['Revenue Growth'].iloc[-1] > 10:
            risk_assessment['Revenue Growth'] = "營收成長強勁"
        else:
            risk_assessment['Revenue Growth'] = "營收成長趨緩"
            
        return risk_assessment