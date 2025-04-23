"""
Financial data loader module for fetching financial statements from TWSE.
This module handles the retrieval and caching of financial data.
"""

from pathlib import Path
import time
import logging
from typing import Dict, Any, Optional
import pandas as pd
import requests
from io import StringIO

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_RETRY_COUNT = 3
DEFAULT_SLEEP_TIME = 2.0

class Config:
    """Configuration settings for the data loader."""
    
    # Data storage paths
    RAW_DIR = Path("data/raw")
    
    # URL templates for different statement types
    URLS = {
        "is": "https://mops.twse.com.tw/nas/t21/{TYPEK}/t163sb04_{rocYear}_{season}_0.csv",   # Income Statement
        "bs": "https://mops.twse.com.tw/nas/t21/{TYPEK}/t163sb05_{rocYear}_{season}_0.csv",   # Balance Sheet
    }
    
    # HTTP request headers
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "zh-TW,zh;q=0.9",
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
        self.session.headers.update(Config.HEADERS | {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
        })
    
    @staticmethod
    def _roc_year(year: int) -> int:
        """Convert Gregorian year to ROC year."""
        return year - 1911
    
    def _build_payload(self, year: int, season: int, market: str = "sii") -> Dict[str, str]:
        """
        Build request payload for TWSE API.
        
        Parameters
        ----------
        year : int
            Gregorian year, e.g. 2023
        season : int
            Quarter (1-4)
        market : str
            Market type ('sii' or 'otc')
            
        Returns
        -------
        Dict[str, str]
            Request payload
        """
        return {
            "encodeURIComponent": "1", 
            "step": "1", 
            "firstin": "1", 
            "off": "1",
            "TYPEK": market,
            "year": str(self._roc_year(year)),
            "season": f"{season:02d}",
        }
    
    def fetch_statement(self, 
                        year: int, 
                        season: int, 
                        table_type: str, 
                        retry: int = DEFAULT_RETRY_COUNT, 
                        sleep_time: float = DEFAULT_SLEEP_TIME) -> Optional[pd.DataFrame]:
        """
        Download a quarterly statement table (income-statement or balance-sheet).

        Parameters
        ----------
        year : int
            Gregorian year, e.g. 2023
        season : int
            Quarter (1-4)
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
        if table_type not in Config.URLS:
            raise ValueError(f"table_type must be one of {list(Config.URLS.keys())}")
        
        # Check if cached file exists
        csv_path = Config.RAW_DIR / f"{table_type}_{year}_{season}.csv"
        if csv_path.exists():
            logger.info(f"Loading cached data: {csv_path}")
            return pd.read_csv(csv_path, index_col=0)
        
        # Set referer based on table type
        referer_page = f"https://mops.twse.com.tw/mops/web/t163sb{'04' if table_type == 'is' else '05'}"
        ajax_url = Config.URLS[table_type]
        
        # Attempt to fetch data with retries
        for attempt in range(retry):
            # Warm-up: fetch the normal HTML page once to obtain cookies
            if attempt == 0:
                try:
                    self.session.get(referer_page, timeout=15)
                except requests.RequestException as e:
                    logger.warning(f"Warm-up request failed: {e}")
            
            # Prepare headers for the actual request
            headers = {
                **self.session.headers,
                "Referer": referer_page,
                "Origin": "https://mops.twse.com.tw",
                "X-Requested-With": "XMLHttpRequest",
            }
            
            try:
                logger.info(f"Fetching {table_type} for {year}Q{season}, attempt {attempt+1}/{retry}")
                payload = self._build_payload(year, season)
                resp = self.session.post(ajax_url, payload, headers=headers, timeout=30)
            except requests.RequestException as e:
                logger.warning(f"Request failed: {e}")
                time.sleep(sleep_time * (attempt + 1))
                continue
            
            # Set encoding and check response
            resp.encoding = "utf8"
            text = resp.text
            
            if "THE PAGE CANNOT BE ACCESSED" in text:
                logger.warning("Access blocked, backing off...")
                time.sleep(sleep_time * (attempt + 1))
                continue
            
            # Try parsing with different parsers
            for parser in ("lxml", "html5lib"):
                try:
                    dfs = pd.read_html(StringIO(text), header=None, flavor=parser)
                    if len(dfs) >= 2:
                        df = (
                            pd.concat(dfs[1:], ignore_index=True)
                            .iloc[:, :-1]
                            .set_index(dfs[1].columns[0])
                            .apply(pd.to_numeric, errors="coerce")
                        )
                        # Cache the result
                        df.to_csv(csv_path)
                        logger.info(f"Successfully fetched and saved {table_type} for {year}Q{season}")
                        return df
                except ValueError:
                    logger.debug(f"Parser {parser} failed to find tables")
                    continue
            
            # If we reach here, either table not yet published or blocked; wait & retry
            logger.warning(f"Failed to parse data, waiting before retry...")
            time.sleep(sleep_time * (attempt + 1))
        
        # If all attempts fail
        error_msg = f"Failed to fetch financial data: {table_type} {year}Q{season}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


def load_financial_data(company_id: str, start_year: int = 2018, end_year: int = 2023) -> pd.DataFrame:
    """
    Load and combine financial data for a specific company.
    
    Parameters
    ----------
    company_id : str
        Company stock code
    start_year : int
        Start year for data collection
    end_year : int
        End year for data collection
        
    Returns
    -------
    pd.DataFrame
        Combined financial data
    """
    # Implementation would go here
    # This is a placeholder for the interface that would be used in app.py
    pass


# Initialize the module when imported
Config.initialize()

# Create a singleton fetcher instance
_fetcher = TWStockDataFetcher()

# Public API functions
def fetch_statement(*args, **kwargs):
    """Public wrapper for TWStockDataFetcher.fetch_statement."""
    return _fetcher.fetch_statement(*args, **kwargs)


if __name__ == "__main__":
    # Set up logging for standalone execution
    logging.basicConfig(level=logging.INFO, 
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Example usage
    try:
        df = fetch_statement(2023, 3, "is")
        print("=== Sample Data ===")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")