import pytest
import pandas as pd
import numpy as np
from finance_analyzer.analysis.indicators import FinancialIndicators

@pytest.fixture
def sample_data():
    """Create sample financial data for testing."""
    # Create sample balance sheet data
    bs_data = pd.DataFrame({
        "資產總額": [1000, 1100, 1200, 1300],  # Total Assets
        "負債總額": [400, 440, 480, 520],      # Total Liabilities
        "權益總額": [600, 660, 720, 780]       # Total Equity
    })
    
    # Create sample income statement data
    is_data = pd.DataFrame({
        "本期淨利（損）": [60, 66, 72, 78],    # Net Income
        "營業收入": [500, 550, 600, 650],      # Revenue
        "營業成本": [300, 330, 360, 390]       # Operating Cost
    })
    
    return bs_data, is_data

def test_calculate_roe(sample_data):
    """Test ROE calculation."""
    bs_data, is_data = sample_data
    roe = FinancialIndicators.calculate_roe(bs_data, is_data)
    
    # Calculate expected ROE values
    expected_roe = (is_data["本期淨利（損）"] / bs_data["權益總額"]) * 100
    
    # Compare calculated and expected values
    pd.testing.assert_series_equal(roe, expected_roe.round(2))

def test_calculate_debt_ratio(sample_data):
    """Test debt ratio calculation."""
    bs_data, _ = sample_data
    debt_ratio = FinancialIndicators.calculate_debt_ratio(bs_data)
    
    # Calculate expected debt ratio values
    expected_debt_ratio = (bs_data["負債總額"] / bs_data["資產總額"]) * 100
    
    # Compare calculated and expected values
    pd.testing.assert_series_equal(debt_ratio, expected_debt_ratio.round(2))

def test_calculate_operating_margin(sample_data):
    """Test operating margin calculation."""
    _, is_data = sample_data
    operating_margin = FinancialIndicators.calculate_operating_margin(is_data)
    
    # Calculate expected operating margin values
    revenue = is_data["營業收入"]
    operating_cost = is_data["營業成本"]
    expected_operating_margin = ((revenue - operating_cost) / revenue) * 100
    
    # Compare calculated and expected values
    pd.testing.assert_series_equal(operating_margin, expected_operating_margin.round(2))

def test_edge_cases():
    """Test edge cases and error handling."""
    # Test with empty DataFrames
    empty_df = pd.DataFrame()
    with pytest.raises(KeyError):
        FinancialIndicators.calculate_roe(empty_df, empty_df)
    
    # Test with zero values
    bs_data = pd.DataFrame({
        "資產總額": [1000, 0, 1200],
        "負債總額": [400, 440, 480],
        "權益總額": [600, 660, 0]
    })
    
    is_data = pd.DataFrame({
        "本期淨利（損）": [60, 66, 72],
        "營業收入": [500, 0, 600],
        "營業成本": [300, 330, 360]
    })
    
    # Test division by zero handling
    with pytest.raises(ZeroDivisionError):
        FinancialIndicators.calculate_roe(bs_data, is_data)
    
    with pytest.raises(ZeroDivisionError):
        FinancialIndicators.calculate_operating_margin(is_data)