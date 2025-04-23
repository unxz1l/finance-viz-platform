"""
Configuration management module.

This module manages application-wide settings and configuration.
It provides a centralized place for constants, file paths, and application settings.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import json


class AppConfig:
    """Application configuration manager."""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        "data_paths": {
            "raw_dir": "data/raw",
            "processed_dir": "data/processed",
            "cache_dir": "data/cache",
        },
        "api": {
            "base_url": "https://mops.twse.com.tw/nas/t21",
            "timeout": 30,
            "retry_count": 3,
            "retry_delay": 2.0,
        },
        "parsing": {
            "preferred_parser": "lxml",
            "fallback_parser": "html5lib",
        },
        "display": {
            "theme": "default",
            "default_indicators": ["ROE", "ROA", "營業利益率", "淨利率"],
            "chart_width": 10,
            "chart_height": 6,
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "finance_analyzer.log",
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Parameters
        ----------
        config_path : str, optional
            Path to configuration file (JSON)
        """
        # Default configuration
        self.config = self.DEFAULT_CONFIG.copy()
        
        # Load from file if provided
        if config_path:
            self.load_from_file(config_path)
        
        # Set up logging
        self._setup_logging()
        
        # Create necessary directories
        self._create_directories()
    
    def load_from_file(self, config_path: str) -> bool:
        """
        Load configuration from a JSON file.
        
        Parameters
        ----------
        config_path : str
            Path to configuration file
            
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                
            # Update configuration
            self._update_config_recursively(self.config, loaded_config)
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading configuration: {e}")
            return False
    
    def _update_config_recursively(self, base_config: Dict, new_config: Dict) -> None:
        """
        Update configuration recursively.
        
        Parameters
        ----------
        base_config : Dict
            Base configuration to update
        new_config : Dict
            New configuration values
        """
        for key, value in new_config.items():
            if key in base_config and isinstance(base_config[key], dict) and isinstance(value, dict):
                self._update_config_recursively(base_config[key], value)
            else:
                base_config[key] = value
    
    def save_to_file(self, config_path: str) -> bool:
        """
        Save current configuration to a JSON file.
        
        Parameters
        ----------
        config_path : str
            Path to save configuration
            
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
                
            return True
        except IOError as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Parameters
        ----------
        section : str
            Configuration section
        key : str
            Configuration key
        default : Any, optional
            Default value if not found
            
        Returns
        -------
        Any
            Configuration value
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Parameters
        ----------
        section : str
            Configuration section
        key : str
            Configuration key
        value : Any
            Value to set
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
    
    def _setup_logging(self) -> None:
        """Configure logging based on configuration."""
        log_config = self.config["logging"]
        
        log_level = getattr(logging, log_config["level"], logging.INFO)
        log_format = log_config["format"]
        log_file = log_config.get("file")
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=log_format,
            filename=log_file,
            filemode='a'
        )
        
        # Create console handler if log file is specified
        if log_file:
            console = logging.StreamHandler()
            console.setLevel(log_level)
            formatter = logging.Formatter(log_format)
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
    
    def _create_directories(self) -> None:
        """Create necessary directories for data storage."""
        for path_key, path_value in self.config["data_paths"].items():
            if path_value:
                Path(path_value).mkdir(parents=True, exist_ok=True)
    
    @property
    def raw_dir(self) -> Path:
        """Get the raw data directory path."""
        return Path(self.config["data_paths"]["raw_dir"])
    
    @property
    def processed_dir(self) -> Path:
        """Get the processed data directory path."""
        return Path(self.config["data_paths"]["processed_dir"])
    
    @property
    def cache_dir(self) -> Path:
        """Get the cache directory path."""
        return Path(self.config["data_paths"]["cache_dir"])
    
    @property
    def api_base_url(self) -> str:
        """Get the API base URL."""
        return self.config["api"]["base_url"]
    
    @property
    def display_theme(self) -> str:
        """Get the display theme."""
        return self.config["display"]["theme"]
    
    @property
    def default_indicators(self) -> list:
        """Get the default indicators list."""
        return self.config["display"]["default_indicators"]


# Create a singleton instance
config = AppConfig()


def get_config() -> AppConfig:
    """
    Get the application configuration instance.
    
    Returns
    -------
    AppConfig
        The application configuration instance
    """
    return config


if __name__ == "__main__":
    # Example usage
    cfg = get_config()
    
    # Get configuration values
    raw_dir = cfg.raw_dir
    timeout = cfg.get("api", "timeout")
    
    print(f"Raw data directory: {raw_dir}")
    print(f"API timeout: {timeout} seconds")
    
    # Set a new value
    cfg.set("api", "timeout", 45)
    print(f"New API timeout: {cfg.get('api', 'timeout')} seconds")