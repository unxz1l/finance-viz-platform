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

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_RETRY_COUNT = 3
DEFAULT_SLEEP_TIME = 2.0

class Config:
    """Configuration settings for the data loader."""
    
    # Data storage paths
    RAW_DIR = Path("data/raw")
    
    # API endpoints
    API_BASE_URL = "https://openapi.twse.com.tw/v1"
    API_ENDPOINTS = {
        "is": "/opendata/t187ap06_X_ci",  # Income Statement
        "bs": "/opendata/t187ap07_X_ci",  # Balance Sheet
    }
    
    # HTTP request headers
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }
    
    # Create data directories if they don't exist
    @classmethod
    def initialize(cls):
        """Create necessary directories for data storage."""
        cls.RAW_DIR.mkdir(parents=True, exist_ok=True)


class TWStockDataFetcher:
    """Class for fetching financial data from Taiwan Stock Exchange."""
    
    def __init__(self):
        """Initialize the fetcher with a persistent session."""
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
    
    def fetch_statement(self, 
                        table_type: str, 
                        retry: int = DEFAULT_RETRY_COUNT, 
                        sleep_time: float = DEFAULT_SLEEP_TIME) -> Optional[pd.DataFrame]:
        """
        Download financial statement table (income-statement or balance-sheet).

        Parameters
        ----------
        table_type : str
            "is" for income-statement, "bs" for balance-sheet
        retry : int
            Number of retry attempts
        sleep_time : float
            Base sleep time between retries (will increase with each retry)
            
        Returns
        -------
        pd.DataFrame or None
            Parsed financial statement dataframe or None if failed
            
        Raises
        ------
        ValueError
            If table_type is invalid
        RuntimeError
            If all fetch attempts fail
        """
        # Validate input
        if table_type not in Config.API_ENDPOINTS:
            raise ValueError(f"table_type must be one of {list(Config.API_ENDPOINTS.keys())}")
        
        # Get current date for cache file
        current_date = datetime.now().strftime("%Y%m%d")
        csv_path = Config.RAW_DIR / f"{table_type}_{current_date}.csv"
        
        # Check if cached file exists and is from today
        if csv_path.exists():
            logger.info(f"Loading cached data: {csv_path}")
            return pd.read_csv(csv_path, index_col=0)
        
        # Build API URL
        api_url = f"{Config.API_BASE_URL}{Config.API_ENDPOINTS[table_type]}"
        
        # Attempt to fetch data with retries
        for attempt in range(retry):
            try:
                logger.info(f"Fetching {table_type} data, attempt {attempt+1}/{retry}")
                resp = self.session.get(api_url, timeout=30)
                logger.info(f"Response status: {resp.status_code}")
                
                if resp.status_code != 200:
                    logger.warning(f"API request failed with status {resp.status_code}")
                    time.sleep(sleep_time * (attempt + 1))
                    continue
                
                # Parse JSON response
                data = resp.json()
                
                if not data:
                    logger.warning("API returned empty data")
                    time.sleep(sleep_time * (attempt + 1))
                    continue
                
                # Convert to DataFrame
                df = pd.DataFrame(data)
                
                # Set company code as index
                if '公司代號' in df.columns:
                    df = df.set_index('公司代號')
                
                # Cache the result
                df.to_csv(csv_path)
                logger.info(f"Successfully fetched and saved {table_type} data")
                return df
                
            except requests.RequestException as e:
                logger.warning(f"Request failed: {e}")
                time.sleep(sleep_time * (attempt + 1))
                continue
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                time.sleep(sleep_time * (attempt + 1))
                continue
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(sleep_time * (attempt + 1))
                continue
        
        # If all attempts fail
        error_msg = f"Failed to fetch financial data: {table_type}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


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
    
    # Sample companies - replace with actual data source
    COMPANIES = [
        "2727 王品餐飲",
        "2729 瓦城泰統",
        "2753 八方雲集",
        "1260 乾杯",
        "1259 安心食品服務",
        "1268 漢來美食",
        "7708 全家國際餐飲",
        "1277 三商餐飲",
        "2752 豆府",
        "4419 皇家可口"
    ]
    
    @staticmethod
    def get_available_companies() -> List[str]:
        """Return list of available companies."""
        return DataLoader.COMPANIES
    
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
            
            # Fetch data from TWSE
            is_df = fetch_statement("is")
            bs_df = fetch_statement("bs")
            
            if is_df is not None and bs_df is not None:
                # Combine income statement and balance sheet data
                if stock_code in is_df.index and stock_code in bs_df.index:
                    combined_df = pd.concat([
                        is_df.loc[[stock_code]],
                        bs_df.loc[[stock_code]]
                    ], axis=1)
                    return combined_df
            
            # If TWSE fetch fails, return sample data
            logger.warning(f"Using sample data for {company}")
            return pd.DataFrame({
                'year': [2019, 2020, 2021, 2022, 2023],
                'ROE': [0.15, 0.18, 0.20, 0.22, 0.25],
                'Operating_Margin': [0.20, 0.22, 0.25, 0.27, 0.30],
                'Debt_Ratio': [0.45, 0.42, 0.40, 0.38, 0.35],
                'Revenue_Growth': [0.05, 0.08, 0.12, 0.15, 0.18]
            })
            
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