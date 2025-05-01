"""
Data processing module for financial data transformation and analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
import logging

# Configure logging
logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles data processing and transformation for financial data."""
    
    @staticmethod
    def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize financial data.
        
        Parameters
        ----------
        df : pd.DataFrame
            Raw financial data
            
        Returns
        -------
        pd.DataFrame
            Cleaned and standardized data
        """
        try:
            # 複製資料以避免修改原始資料
            df = df.copy()
            
            # 轉換數值欄位
            numeric_columns = ['DividendYield', 'PEratio', 'PBratio', 'YieldRatio']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 處理缺失值
            df = df.replace([np.inf, -np.inf], np.nan)
            
            # 計算額外指標
            if 'DividendYield' in df.columns and 'PEratio' in df.columns:
                df['DividendPE'] = df['DividendYield'] * df['PEratio']
            
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning financial data: {str(e)}")
            raise
    
    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate key financial metrics.
        
        Parameters
        ----------
        df : pd.DataFrame
            Cleaned financial data
            
        Returns
        -------
        Dict[str, float]
            Dictionary of calculated metrics
        """
        try:
            metrics = {}
            
            # 基本指標
            if 'DividendYield' in df.columns:
                metrics['dividend_yield'] = df['DividendYield'].mean()
            
            if 'PEratio' in df.columns:
                metrics['pe_ratio'] = df['PEratio'].mean()
            
            if 'PBratio' in df.columns:
                metrics['pb_ratio'] = df['PBratio'].mean()
            
            # 計算變異性
            if 'DividendYield' in df.columns:
                metrics['dividend_volatility'] = df['DividendYield'].std()
            
            if 'PEratio' in df.columns:
                metrics['pe_volatility'] = df['PEratio'].std()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            raise
    
    @staticmethod
    def prepare_visualization_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare data for visualization.
        
        Parameters
        ----------
        df : pd.DataFrame
            Cleaned financial data
            
        Returns
        -------
        pd.DataFrame
            Data formatted for visualization
        """
        try:
            # 選擇需要的欄位
            columns = ['Name', 'DividendYield', 'PEratio', 'PBratio', 'YieldRatio']
            columns = [col for col in columns if col in df.columns]
            
            # 轉換為長格式
            df_long = df[columns].melt(
                id_vars=['Name'],
                var_name='Metric',
                value_name='Value'
            )
            
            return df_long
            
        except Exception as e:
            logger.error(f"Error preparing visualization data: {str(e)}")
            raise
