import logging
from finance_analyzer.data.loader import fetch_statement
import pandas as pd
import pytest
from pathlib import Path
import os
from finance_analyzer.data.loader import TWStockDataFetcher, Config, DataLoader
from unittest.mock import patch, MagicMock
import json

# 設定日誌
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture
def mock_response():
    """Create a mock API response."""
    return [
        {
            "Code": "2727",
            "Name": "王品",
            "PEratio": "25.80",
            "DividendYield": "2.34",
            "PBratio": "3.45"
        },
        {
            "Code": "2729",
            "Name": "瓦城",
            "PEratio": "28.50",
            "DividendYield": "1.98",
            "PBratio": "4.12"
        }
    ]

@pytest.fixture
def mock_cache_dir(tmp_path):
    """Create a temporary cache directory."""
    cache_dir = tmp_path / "finance-viz-platform" / "raw"
    cache_dir.mkdir(parents=True)
    return cache_dir

def test_config_initialization():
    """Test configuration initialization."""
    Config.initialize()
    assert Config.RAW_DIR.exists()
    assert isinstance(Config.TWSE_HEADERS, dict)
    assert isinstance(Config.TPEX_HEADERS, dict)

@patch('requests.Session')
def test_fetch_statement_twse(mock_session, mock_response, mock_cache_dir):
    """Test fetching statement from TWSE."""
    # Setup mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = mock_response
    mock_session.return_value.get.return_value = mock_resp
    
    # Initialize fetcher with mock cache dir
    with patch('finance_analyzer.data.loader.Config.RAW_DIR', mock_cache_dir):
        fetcher = TWStockDataFetcher()
        df = fetcher.fetch_statement("is", market="twse")
    
    assert df is not None
    assert len(df) == 2
    assert "2727" in df.index
    assert "PEratio" in df.columns

@patch('requests.Session')
def test_fetch_statement_tpex(mock_session, mock_response, mock_cache_dir):
    """Test fetching statement from TPEx."""
    # Setup mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = mock_response
    mock_session.return_value.get.return_value = mock_resp
    
    # Initialize fetcher with mock cache dir
    with patch('finance_analyzer.data.loader.Config.RAW_DIR', mock_cache_dir):
        fetcher = TWStockDataFetcher()
        df = fetcher.fetch_statement("is", market="tpex")
    
    assert df is not None
    assert len(df) == 2
    assert "2727" in df.index
    assert "PEratio" in df.columns

def test_data_loader():
    """Test DataLoader functionality."""
    # Test getting available companies
    companies = DataLoader.get_available_companies()
    assert isinstance(companies, list)
    assert len(companies) > 0
    assert all(isinstance(company, str) for company in companies)
    
    # Test loading company data
    company = companies[0]
    with patch('finance_analyzer.data.loader.fetch_statement') as mock_fetch:
        mock_fetch.return_value = pd.DataFrame({
            'PEratio': [25.80],
            'DividendYield': [2.34],
            'PBratio': [3.45]
        }, index=['2727'])
        
        data = DataLoader.load_company_data(company)
        assert data is not None
        assert isinstance(data, pd.DataFrame)
        assert not data.empty

def test_error_handling():
    """Test error handling in data loading."""
    fetcher = TWStockDataFetcher()
    
    # Test invalid market
    with pytest.raises(ValueError):
        fetcher.fetch_statement("is", market="invalid")
    
    # Test invalid table type
    with pytest.raises(ValueError):
        fetcher.fetch_statement("invalid", market="twse")
    
    # Test API error with 404 response
    with patch('requests.Session') as mock_session:
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_session.return_value.get.return_value = mock_resp
        
        with pytest.raises(RuntimeError):
            fetcher.fetch_statement("is", market="twse", retry=1)

def test_cache_functionality(mock_cache_dir):
    """Test data caching functionality."""
    # Create mock cache file
    current_date = pd.Timestamp.now().strftime("%Y%m%d")
    cache_file = mock_cache_dir / f"twse_is_{current_date}.csv"
    
    mock_data = pd.DataFrame({
        'PEratio': [25.80],
        'DividendYield': [2.34],
        'PBratio': [3.45]
    }, index=['2727'])
    
    mock_data.to_csv(cache_file)
    
    # Test cache loading
    with patch('finance_analyzer.data.loader.Config.RAW_DIR', mock_cache_dir):
        fetcher = TWStockDataFetcher()
        df = fetcher.fetch_statement("is", market="twse")
    
    assert df is not None
    assert not df.empty
    assert "2727" in df.index

def test_fetch_restaurant_companies():
    """Test fetching restaurant company data."""
    # Test restaurant companies list
    restaurant_companies = [
        "2727",  # 王品
        "2729",  # 瓦城
        "2753",  # 八方雲集
        "1259",  # 安心食品服務
        "1268",  # 漢來美食
        "7708",  # 全家國際餐飲
        "7705",  # 三商餐飲
        "2752",  # 豆府
        "4419",  # 皇家可口
        "2723",  # 美食-KY
        "2732"   # 六角國際
    ]
    
    # Test that all companies are in the DataLoader.COMPANIES list
    company_codes = [company["code"] for company in DataLoader.COMPANIES]
    for code in restaurant_companies:
        assert code in company_codes

if __name__ == "__main__":
    test_fetch_restaurant_companies()