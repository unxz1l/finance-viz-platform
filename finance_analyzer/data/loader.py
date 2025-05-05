"""
Financial data loader module for fetching financial statements from TWSE.
This module handles the retrieval and caching of financial data.
"""

from pathlib import Path
import time
import logging
from typing import Dict, Any, Optional, List
import pandas as pd
import requests
from io import StringIO
import streamlit as st
import json
from datetime import datetime
import os
from appdirs import user_cache_dir

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_RETRY_COUNT = 3
DEFAULT_SLEEP_TIME = 2.0

# 設定快取目錄
CACHE_DIR = user_cache_dir('finance-viz-platform', 'nthu')
os.makedirs(CACHE_DIR, exist_ok=True)

class Config:
    """Configuration settings for the data loader."""
    
    # Data storage paths
    RAW_DIR = Path(CACHE_DIR) / "raw"
    
    # API endpoints
    TWSE_BASE_URL = "https://openapi.twse.com.tw/v1"
    TPEX_BASE_URL = "https://www.tpex.org.tw/openapi/v1"
    
    API_ENDPOINTS = {
        "twse": {
            "is": "/exchangeReport/BWIBBU_d",  # Income Statement
            "bs": "/exchangeReport/BWIBBU_d",  # Balance Sheet
        },
        "tpex": {
            "is": "/tpex_mainboard_peratio_analysis",  # Income Statement
            "bs": "/tpex_mainboard_peratio_analysis",  # Balance Sheet
        }
    }
    
    # Column mappings for different markets
    COLUMN_MAPPINGS = {
        "twse": {
            "Code": "Code",
            "Name": "Name",
            "PEratio": "PEratio",
            "DividendYield": "DividendYield",
            "PBratio": "PBratio"
        },
        "tpex": {
            "SecuritiesCompanyCode": "Code",
            "CompanyName": "Name",
            "PriceEarningRatio": "PEratio",
            "DividendPerShare": "DividendYield",
            "PriceBookRatio": "PBratio"
        }
    }
    
    # HTTP request headers
    TWSE_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    TPEX_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    # Create data directories if they don't exist
    @classmethod
    def initialize(cls):
        """Create necessary directories for data storage."""
        cls.RAW_DIR.mkdir(parents=True, exist_ok=True)


class TWStockDataFetcher:
    """Class for fetching financial data from Taiwan Stock Exchange and TPEX."""
    
    def __init__(self):
        """Initialize the fetcher with a persistent session."""
        self.session = requests.Session()
        self.session.headers.update(Config.TWSE_HEADERS)
    
    def fetch_statement(self, 
                        table_type: str,
                        market: str = "twse",  # "twse" or "tpex"
                        retry: int = DEFAULT_RETRY_COUNT, 
                        sleep_time: float = DEFAULT_SLEEP_TIME) -> Optional[pd.DataFrame]:
        """
        Download financial statement table (income-statement or balance-sheet).

        Parameters
        ----------
        table_type : str
            "is" for income-statement, "bs" for balance-sheet
        market : str
            "twse" for listed companies, "tpex" for OTC companies
        retry : int
            Number of retry attempts
        sleep_time : float
            Base sleep time between retries (will increase with each retry)
            
        Returns
        -------
        pd.DataFrame or None
            Parsed financial statement dataframe or None if failed
        """
        # Validate input
        if market not in Config.API_ENDPOINTS:
            raise ValueError(f"market must be one of {list(Config.API_ENDPOINTS.keys())}")
        if table_type not in Config.API_ENDPOINTS[market]:
            raise ValueError(f"table_type must be one of {list(Config.API_ENDPOINTS[market].keys())}")
        
        # Get current date for cache file
        current_date = datetime.now().strftime("%Y%m%d")
        csv_path = Config.RAW_DIR / f"{market}_{table_type}_{current_date}.csv"
        
        # Check if cached file exists and is from today
        if csv_path.exists():
            try:
                df = pd.read_csv(csv_path)
                if not df.empty:
                    column_mapping = Config.COLUMN_MAPPINGS[market]
                    df = df.rename(columns=column_mapping)
                    df = df.set_index("Code")
                    df.index = df.index.astype(str)
                    return df
            except Exception:
                pass
        
        # Build API URL
        base_url = Config.TWSE_BASE_URL if market == "twse" else Config.TPEX_BASE_URL
        api_url = f"{base_url}{Config.API_ENDPOINTS[market][table_type]}"
        
        # Set appropriate headers
        headers = Config.TWSE_HEADERS if market == "twse" else Config.TPEX_HEADERS
        self.session.headers.update(headers)
        
        # Attempt to fetch data with retries
        for attempt in range(retry):
            try:
                resp = self.session.get(api_url, timeout=30)
                if resp.status_code != 200:
                    time.sleep(sleep_time * (attempt + 1))
                    continue
                
                data = resp.json()
                if not data:
                    time.sleep(sleep_time * (attempt + 1))
                    continue
                
                # Create DataFrame and rename columns
                df = pd.DataFrame(data)
                column_mapping = Config.COLUMN_MAPPINGS[market]
                df = df.rename(columns=column_mapping)
                df = df.set_index("Code")
                df.index = df.index.astype(str)
                
                # Cache the result
                df.to_csv(csv_path)
                return df
                
            except Exception:
                time.sleep(sleep_time * (attempt + 1))
                continue
        
        return None


# Initialize the module when imported
Config.initialize()

# Create a singleton fetcher instance
_fetcher = TWStockDataFetcher()

# Public API functions
def fetch_statement(*args, **kwargs):
    """Public wrapper for TWStockDataFetcher.fetch_statement."""
    return _fetcher.fetch_statement(*args, **kwargs)


class DataLoader:
    """Handles data loading and caching for financial data."""
    
    # Sample companies with market information
    COMPANIES = [
    {"code": "2727", "name": "王品股份有限公司", "market": "twse"},
    {"code": "2729", "name": "瓦城泰統股份有限公司", "market": "twse"},
    {"code": "2753", "name": "八方雲集國際股份有限公司", "market": "twse"},
    {"code": "1259", "name": "安心食品服務股份有限公司", "market": "tpex"},
    {"code": "1268", "name": "漢來美食股份有限公司", "market": "tpex"},
    {"code": "7708", "name": "全家國際餐飲股份有限公司", "market": "tpex"},
    {"code": "7705", "name": "三商餐飲股份有限公司", "market": "twse"},
    {"code": "2752", "name": "豆府股份有限公司", "market": "tpex"},
    {"code": "4419", "name": "皇家國際美食股份有限公司", "market": "tpex"},
    {"code": "2723", "name": "美食-KY股份有限公司", "market": "twse"},
    {"code": "2732", "name": "六角國際事業股份有限公司", "market": "tpex"}
]

    @staticmethod
    def get_available_companies() -> List[str]:
        """Return list of available companies."""
        return [f"{company['code']} {company['name']}" for company in DataLoader.COMPANIES]
    
    @staticmethod
    @st.cache_data
    def load_company_data(company: str) -> Optional[pd.DataFrame]:
        """
        Load financial data for a given company.
        
        Parameters
        ----------
        company : str
            Company name and code (e.g., "2330 台積電")
            
        Returns
        -------
        pd.DataFrame or None
            Financial data for the company
        """
        try:
            # Extract stock code
            stock_code = company.split()[0]
            
            # Find company info
            company_info = next((c for c in DataLoader.COMPANIES if c["code"] == stock_code), None)
            if not company_info:
                logger.warning(f"Company {company} not found in the list")
                return None
            
            # Get market from company info
            market = company_info["market"]
            data = None
            error_msg = None
            
            try:
                is_df = fetch_statement("is", market=market)
                bs_df = fetch_statement("bs", market=market)
                
                if is_df is not None and bs_df is not None:
                    # Combine income statement and balance sheet data
                    if stock_code in is_df.index and stock_code in bs_df.index:
                        data = pd.concat([
                            is_df.loc[[stock_code]],
                            bs_df.loc[[stock_code]]
                        ], axis=1)
                        # Add timestamp and market info
                        data['fetch_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        data['market'] = market.upper()
            except Exception as e:
                error_msg = f"Failed to fetch data from {market}: {str(e)}"
                logger.warning(error_msg)
            
            if data is not None:
                return data
            elif error_msg:
                logger.error(error_msg)
                return None
            else:
                logger.warning(f"No data found for company {company}")
                return None
            
        except Exception as e:
            logger.error(f"Error loading data for {company}: {str(e)}")
            return None


if __name__ == "__main__":
    # Set up logging for standalone execution
    logging.basicConfig(level=logging.INFO, 
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Example usage
    try:
        df = fetch_statement("is")
        print("=== Sample Data ===")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")