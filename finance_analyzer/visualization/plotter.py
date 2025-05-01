"""
Visualization module for generating financial charts.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Optional, Union
import logging

# Configure logging
logger = logging.getLogger(__name__)

class FinancialPlotter:
    """Handles generation of financial charts and visualizations."""
    
    @staticmethod
    def _format_metric_name(metric: str) -> str:
        """Format metric name for display."""
        name_map = {
            "ROE": "股東權益報酬率",
            "Revenue Growth": "營收成長率",
            "Operating Margin Growth": "營業淨利成長率"
        }
        return name_map.get(metric, metric)
    
    @staticmethod
    def create_metric_bar_chart(df: pd.DataFrame, metric: str, title: str = None) -> go.Figure:
        """Create a bar chart for a specific financial metric."""
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df.index, y=df[metric]))
        fig.update_layout(
            title=title or f'{metric} Trend',
            xaxis_title='Date',
            yaxis_title=metric
        )
        return fig
    
    @staticmethod
    def create_metric_line_chart(df: pd.DataFrame, metric: str, title: str = None) -> go.Figure:
        """Create a line chart for a specific financial metric."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[metric],
            mode='lines+markers',
            name=FinancialPlotter._format_metric_name(metric)
        ))
        
        # 設定標題和軸標籤
        metric_name = FinancialPlotter._format_metric_name(metric)
        fig.update_layout(
            title=title or f'{metric_name}趨勢',
            xaxis_title='年度',
            yaxis_title=f'{metric_name} (%)',
            template='plotly_white',
            showlegend=True
        )
        
        # 設定Y軸格式
        fig.update_yaxes(ticksuffix='%')
        
        return fig
    
    @staticmethod
    def create_multi_metric_chart(df: pd.DataFrame, metrics: list, title: str = None) -> go.Figure:
        """Create a line chart comparing multiple financial metrics."""
        fig = go.Figure()
        
        # 設定顏色
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        for i, metric in enumerate(metrics):
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[metric],
                mode='lines+markers',
                name=FinancialPlotter._format_metric_name(metric),
                line=dict(color=colors[i % len(colors)])
            ))
        
        fig.update_layout(
            title=title or '財務指標比較',
            xaxis_title='年度',
            yaxis_title='數值 (%)',
            template='plotly_white',
            showlegend=True,
            hovermode='x unified'
        )
        
        # 設定Y軸格式
        fig.update_yaxes(ticksuffix='%')
        
        return fig
    
    @staticmethod
    def create_metric_scatter_plot(df: pd.DataFrame, x_metric: str, y_metric: str) -> go.Figure:
        """
        Create a scatter plot comparing two metrics.
        
        Parameters
        ----------
        df : pd.DataFrame
            Financial data
        x_metric : str
            Metric for x-axis
        y_metric : str
            Metric for y-axis
            
        Returns
        -------
        go.Figure
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            # 建立散點圖
            fig.add_trace(go.Scatter(
                x=df[x_metric],
                y=df[y_metric],
                mode='markers+text',
                text=df['Name'],
                textposition='top center',
                marker=dict(
                    size=15,
                    color=df[y_metric],
                    colorscale='Viridis',
                    showscale=True
                )
            ))
            
            # 更新佈局
            fig.update_layout(
                title=f'{x_metric} vs {y_metric}',
                xaxis_title=x_metric,
                yaxis_title=y_metric,
                showlegend=False,
                height=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating scatter plot: {str(e)}")
            raise
    
    @staticmethod
    def create_metric_heatmap(df: pd.DataFrame, metrics: List[str]) -> go.Figure:
        """
        Create a heatmap of financial metrics.
        
        Parameters
        ----------
        df : pd.DataFrame
            Financial data
        metrics : List[str]
            List of metrics to include in heatmap
            
        Returns
        -------
        go.Figure
            Plotly figure object
        """
        try:
            # 選擇需要的欄位
            df_metrics = df[metrics]
            
            # 建立熱力圖
            fig = go.Figure(data=go.Heatmap(
                z=df_metrics.values,
                x=metrics,
                y=df['Name'],
                colorscale='Viridis',
                text=df_metrics.round(2).values,
                texttemplate='%{text}',
                textfont={"size": 10}
            ))
            
            # 更新佈局
            fig.update_layout(
                title='Financial Metrics Heatmap',
                xaxis_title='Metrics',
                yaxis_title='Company',
                height=800,
                margin=dict(l=150, r=50, t=50, b=50)
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {str(e)}")
            raise

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

    @staticmethod
    def create_comparison_table(df: pd.DataFrame, year: str) -> pd.DataFrame:
        """Create a comparison table for a specific year."""
        # 轉換年度格式（例如：103 -> 2014）
        year_int = int(year) + 1911
        prev_year = year_int - 1
        
        # 選擇當年度和上一年度的數據
        current_data = df[df.index == year_int]
        prev_data = df[df.index == prev_year]
        
        if current_data.empty or prev_data.empty:
            return pd.DataFrame()
        
        # 創建比較表
        comparison = pd.DataFrame({
            '指標': ['股東權益報酬率', '營收成長率', '營業淨利成長率'],
            f'{year}年': [
                current_data['ROE'].values[0],
                current_data['Revenue Growth'].values[0],
                current_data['Operating Margin Growth'].values[0]
            ],
            f'{int(year)-1}年': [
                prev_data['ROE'].values[0],
                prev_data['Revenue Growth'].values[0],
                prev_data['Operating Margin Growth'].values[0]
            ]
        })
        
        return comparison 