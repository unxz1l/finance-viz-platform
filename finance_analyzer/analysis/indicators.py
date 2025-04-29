"""
Financial indicators calculation module.

This module provides functions to calculate various financial indicators
from balance sheet and income statement data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union, Optional


class FinancialIndicators:
    """Class for calculating financial indicators from financial statements."""
    
    @staticmethod
    def calculate_roe(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame) -> pd.Series:
        """
        Calculate Return on Equity (ROE).
        
        Uses the current period's net income divided by the average of the
        current and previous period's total equity.
        
        Parameters
        ----------
        balance_sheet : pd.DataFrame
            Balance sheet data with 'Total Equity' column
        income_statement : pd.DataFrame
            Income statement data with 'Net Income' column
            
        Returns
        -------
        pd.Series
            ROE values as percentages, rounded to 2 decimal places
        """
        equity = balance_sheet["權益總額"]  # Total Equity
        net_income = income_statement["本期淨利（損）"]  # Net Income
        
        # Use the average of current and previous period's equity
        roe = net_income / (equity.rolling(2).mean()) * 100
        
        return roe.round(2)
    
    @staticmethod
    def calculate_roa(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame) -> pd.Series:
        """
        Calculate Return on Assets (ROA).
        
        Parameters
        ----------
        balance_sheet : pd.DataFrame
            Balance sheet data with 'Total Assets' column
        income_statement : pd.DataFrame
            Income statement data with 'Net Income' column
            
        Returns
        -------
        pd.Series
            ROA values as percentages, rounded to 2 decimal places
        """
        assets = balance_sheet["資產總額"]  # Total Assets
        net_income = income_statement["本期淨利（損）"]  # Net Income
        
        # Use the average of current and previous period's assets
        roa = net_income / (assets.rolling(2).mean()) * 100
        
        return roa.round(2)
    
    @staticmethod
    def calculate_debt_ratio(balance_sheet: pd.DataFrame) -> pd.Series:
        """
        Calculate Debt Ratio (Total Liabilities / Total Assets).
        
        Parameters
        ----------
        balance_sheet : pd.DataFrame
            Balance sheet data with 'Total Liabilities' and 'Total Assets' columns
            
        Returns
        -------
        pd.Series
            Debt ratio values as percentages, rounded to 2 decimal places
        """
        liabilities = balance_sheet["負債總額"]  # Total Liabilities
        assets = balance_sheet["資產總額"]  # Total Assets
        
        debt_ratio = (liabilities / assets) * 100
        
        return debt_ratio.round(2)
    
    @staticmethod
    def calculate_profit_margin(income_statement: pd.DataFrame) -> pd.Series:
        """
        Calculate Net Profit Margin.
        
        Parameters
        ----------
        income_statement : pd.DataFrame
            Income statement data with 'Net Income' and 'Revenue' columns
            
        Returns
        -------
        pd.Series
            Profit margin values as percentages, rounded to 2 decimal places
        """
        net_income = income_statement["本期淨利（損）"]  # Net Income
        revenue = income_statement["營業收入"]  # Revenue
        
        profit_margin = (net_income / revenue) * 100
        
        return profit_margin.round(2)
    
    @staticmethod
    def calculate_revenue_growth(income_statement: pd.DataFrame) -> pd.Series:
        """
        Calculate Revenue Growth Rate.
        
        Parameters
        ----------
        income_statement : pd.DataFrame
            Income statement data with 'Revenue' column
            
        Returns
        -------
        pd.Series
            Revenue growth values as percentages, rounded to 2 decimal places
        """
        revenue = income_statement["營業收入"]  # Revenue
        growth = revenue.pct_change() * 100
        
        return growth.round(2)


def calculate_financial_ratios(balance_sheet: pd.DataFrame, 
                              income_statement: pd.DataFrame) -> Dict[str, pd.Series]:
    """
    Calculate multiple financial ratios at once.
    
    Parameters
    ----------
    balance_sheet : pd.DataFrame
        Balance sheet data
    income_statement : pd.DataFrame
        Income statement data
        
    Returns
    -------
    Dict[str, pd.Series]
        Dictionary of calculated financial ratios
    """
    indicators = FinancialIndicators()
    
    ratios = {
        "ROE": indicators.calculate_roe(balance_sheet, income_statement),
        "ROA": indicators.calculate_roa(balance_sheet, income_statement),
        "Debt Ratio": indicators.calculate_debt_ratio(balance_sheet),
        "Profit Margin": indicators.calculate_profit_margin(income_statement),
        "Revenue Growth": indicators.calculate_revenue_growth(income_statement)
    }
    
    return ratios


if __name__ == "__main__":
    # This section is for testing purposes
    import numpy as np
    
    # Create sample data
    bs_data = pd.DataFrame({
        "權益總額": [1000, 1100, 1200, 1300],
        "資產總額": [1500, 1600, 1700, 1800],
        "負債總額": [500, 500, 500, 500]
    })
    
    is_data = pd.DataFrame({
        "本期淨利（損）": [100, 120, 140, 160],
        "營業收入": [800, 850, 900, 950]
    })
    
    # Test calculations
    indicators = FinancialIndicators()
    roe = indicators.calculate_roe(bs_data, is_data)
    
    print("=== Sample ROE ===")
    print(roe)