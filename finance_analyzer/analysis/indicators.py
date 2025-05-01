"""
Financial indicators calculation module.

This module provides functions to calculate various financial indicators
from balance sheet and income statement data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union, Optional


class FinancialIndicators:
    """Class for calculating financial indicators."""
    
    @staticmethod
    def calculate_roe(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame) -> pd.Series:
        """Calculate Return on Equity (ROE)."""
        equity = balance_sheet["權益總額"]
        net_income = income_statement["本期淨利（損）"]
        return (net_income / equity * 100).round(2)
    
    @staticmethod
    def calculate_debt_ratio(balance_sheet: pd.DataFrame) -> pd.Series:
        """Calculate Debt Ratio."""
        liabilities = balance_sheet["負債總額"]
        assets = balance_sheet["資產總額"]
        return (liabilities / assets * 100).round(2)
    
    @staticmethod
    def calculate_operating_margin(income_statement: pd.DataFrame) -> pd.Series:
        """Calculate Operating Margin."""
        revenue = income_statement["營業收入"]
        operating_cost = income_statement["營業成本"]
        return ((revenue - operating_cost) / revenue * 100).round(2)
    
    @staticmethod
    def calculate_revenue_growth(income_statement: pd.DataFrame) -> pd.Series:
        """Calculate Revenue Growth Rate."""
        revenue = income_statement["營業收入"]
        # 計算年增率
        growth_rate = revenue.pct_change() * 100
        return growth_rate.round(2)
    
    @staticmethod
    def calculate_operating_margin_growth(income_statement: pd.DataFrame) -> pd.Series:
        """Calculate Operating Margin Growth Rate."""
        revenue = income_statement["營業收入"]
        operating_cost = income_statement["營業成本"]
        operating_margin = ((revenue - operating_cost) / revenue * 100)
        # 計算年增率
        growth_rate = operating_margin.pct_change() * 100
        return growth_rate.round(2)


def calculate_financial_ratios(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame) -> dict:
    """Calculate all financial ratios."""
    return {
        "ROE": FinancialIndicators.calculate_roe(balance_sheet, income_statement),
        "Debt Ratio": FinancialIndicators.calculate_debt_ratio(balance_sheet),
        "Operating Margin": FinancialIndicators.calculate_operating_margin(income_statement),
        "Revenue Growth": FinancialIndicators.calculate_revenue_growth(income_statement),
        "Operating Margin Growth": FinancialIndicators.calculate_operating_margin_growth(income_statement)
    }


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