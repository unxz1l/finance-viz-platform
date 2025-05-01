"""
Streamlit dashboard components for financial data visualization.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Union
import logging
from ..data.processor import DataProcessor
from .plotter import FinancialPlotter

# Configure logging
logger = logging.getLogger(__name__)

class FinancialDashboard:
    """Handles Streamlit dashboard components and layout."""
    
    @staticmethod
    def display_company_selector(companies: List[Dict[str, str]]) -> str:
        """
        Display company selection dropdown.
        
        Parameters
        ----------
        companies : List[Dict[str, str]]
            List of company information
            
        Returns
        -------
        str
            Selected company code
        """
        try:
            # 建立選項列表
            options = [f"{company['code']} {company['name']}" for company in companies]
            
            # 顯示下拉選單
            selected = st.selectbox(
                "選擇公司",
                options,
                index=0
            )
            
            # 回傳選擇的公司代碼
            return selected.split()[0]
            
        except Exception as e:
            logger.error(f"Error displaying company selector: {str(e)}")
            raise
    
    @staticmethod
    def display_metrics_summary(metrics: Dict[str, float]):
        """
        Display key financial metrics summary.
        
        Parameters
        ----------
        metrics : Dict[str, float]
            Dictionary of financial metrics
        """
        try:
            # 建立三欄佈局
            col1, col2, col3 = st.columns(3)
            
            # 顯示基本指標
            with col1:
                st.metric("平均殖利率", f"{metrics.get('dividend_yield', 0):.2f}%")
            with col2:
                st.metric("平均本益比", f"{metrics.get('pe_ratio', 0):.2f}")
            with col3:
                st.metric("平均股價淨值比", f"{metrics.get('pb_ratio', 0):.2f}")
            
            # 顯示變異性指標
            with col1:
                st.metric("殖利率波動", f"{metrics.get('dividend_volatility', 0):.2f}%")
            with col2:
                st.metric("本益比波動", f"{metrics.get('pe_volatility', 0):.2f}")
            
        except Exception as e:
            logger.error(f"Error displaying metrics summary: {str(e)}")
            raise
    
    @staticmethod
    def display_comparison_charts(df: pd.DataFrame):
        """
        Display comparison charts for financial metrics.
        
        Parameters
        ----------
        df : pd.DataFrame
            Financial data
        """
        try:
            # 建立標籤頁
            tab1, tab2, tab3 = st.tabs(["長條圖", "散點圖", "熱力圖"])
            
            # 長條圖標籤頁
            with tab1:
                metric = st.selectbox(
                    "選擇指標",
                    ['DividendYield', 'PEratio', 'PBratio'],
                    key='bar_metric'
                )
                fig = FinancialPlotter.create_metric_bar_chart(df, metric)
                st.plotly_chart(fig, use_container_width=True)
            
            # 散點圖標籤頁
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    x_metric = st.selectbox(
                        "X軸指標",
                        ['DividendYield', 'PEratio', 'PBratio'],
                        key='scatter_x'
                    )
                with col2:
                    y_metric = st.selectbox(
                        "Y軸指標",
                        ['DividendYield', 'PEratio', 'PBratio'],
                        key='scatter_y'
                    )
                fig = FinancialPlotter.create_metric_scatter_plot(df, x_metric, y_metric)
                st.plotly_chart(fig, use_container_width=True)
            
            # 熱力圖標籤頁
            with tab3:
                metrics = st.multiselect(
                    "選擇指標",
                    ['DividendYield', 'PEratio', 'PBratio'],
                    default=['DividendYield', 'PEratio', 'PBratio']
                )
                if metrics:
                    fig = FinancialPlotter.create_metric_heatmap(df, metrics)
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            logger.error(f"Error displaying comparison charts: {str(e)}")
            raise
    
    @staticmethod
    def display_raw_data(df: pd.DataFrame):
        """
        Display raw financial data table.
        
        Parameters
        ----------
        df : pd.DataFrame
            Financial data
        """
        try:
            st.subheader("原始資料")
            st.dataframe(df)
            
            # 提供下載選項
            csv = df.to_csv().encode('utf-8')
            st.download_button(
                label="下載 CSV",
                data=csv,
                file_name='financial_data.csv',
                mime='text/csv'
            )
            
        except Exception as e:
            logger.error(f"Error displaying raw data: {str(e)}")
            raise 