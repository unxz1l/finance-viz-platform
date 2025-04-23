"""
Financial data visualization module.

This module provides functions and classes for visualizing financial data
and indicators using matplotlib and other visualization libraries.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union, Optional
import matplotlib.ticker as mtick


class FinancialPlotter:
    """Class for creating financial data visualizations."""
    
    def __init__(self, theme: str = "default"):
        """
        Initialize the plotter with a specific visual theme.
        
        Parameters
        ----------
        theme : str
            Visual theme to use ('default', 'light', 'dark', 'corporate')
        """
        # Set up default plotting style
        self.theme = theme
        self._setup_style()
        
    def _setup_style(self):
        """Configure matplotlib style based on theme."""
        if self.theme == "default":
            plt.style.use('seaborn-v0_8-whitegrid')
        elif self.theme == "dark":
            plt.style.use('dark_background')
        elif self.theme == "corporate":
            plt.style.use('ggplot')
        else:  # light
            plt.style.use('seaborn-v0_8')
        
        # Set default figure size
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 12
        
    def plot_indicator_trend(self, 
                           time_series: pd.Series, 
                           indicator_name: str,
                           company_name: str = "",
                           include_avg: bool = False,
                           show_grid: bool = True) -> plt.Figure:
        """
        Plot a time series of a financial indicator.
        
        Parameters
        ----------
        time_series : pd.Series
            Time series data with datetime index
        indicator_name : str
            Name of the indicator (used for title and y-axis)
        company_name : str, optional
            Company name for title
        include_avg : bool, optional
            Whether to include a horizontal line for the average value
        show_grid : bool, optional
            Whether to show grid lines
            
        Returns
        -------
        plt.Figure
            The matplotlib figure object
        """
        # Create figure and axis
        fig, ax = plt.subplots()
        
        # Plot the data
        ax.plot(time_series.index, time_series.values, marker='o', 
              linestyle='-', linewidth=2, markersize=8)
        
        # Add average line if requested
        if include_avg and len(time_series) > 0:
            avg_value = time_series.mean()
            ax.axhline(y=avg_value, color='r', linestyle='--', alpha=0.7)
            ax.text(time_series.index[0], avg_value, 
                  f'平均: {avg_value:.2f}', 
                  va='bottom', ha='left', alpha=0.7)
        
        # Set labels and title
        title = f"{indicator_name} 趨勢"
        if company_name:
            title = f"{company_name} - {title}"
            
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel("日期", fontsize=12)
        ax.set_ylabel(indicator_name, fontsize=12)
        
        # Format y-axis as percentage if appropriate
        if any(kw in indicator_name.lower() for kw in ['率', 'roe', 'roa', '%']):
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
        
        # Show grid if requested
        if show_grid:
            ax.grid(True, alpha=0.3)
            
        # Add data labels
        for x, y in zip(time_series.index, time_series.values):
            ax.annotate(f'{y:.2f}', (x, y), xytext=(0, 5), 
                      textcoords='offset points', ha='center')
        
        # Adjust layout
        fig.tight_layout()
        
        return fig
    
    def plot_comparison(self, 
                      data: pd.DataFrame, 
                      indicator: str,
                      companies: List[str] = None,
                      title: str = "",
                      use_bar: bool = False) -> plt.Figure:
        """
        Plot comparison of an indicator across multiple companies or time periods.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data containing the indicator values
        indicator : str
            Column name of the indicator to plot
        companies : List[str], optional
            List of companies to include (if None, use all)
        title : str, optional
            Custom title for the plot
        use_bar : bool, optional
            Whether to use bar chart instead of line chart
            
        Returns
        -------
        plt.Figure
            The matplotlib figure object
        """
        # Filter data if companies specified
        if companies:
            data = data[data.index.isin(companies)]
            
        # Create figure
        fig, ax = plt.subplots()
        
        # Create plot based on type
        if use_bar:
            data[indicator].plot(kind='bar', ax=ax, rot=45)
            
            # Add data labels on bars
            for i, v in enumerate(data[indicator]):
                ax.text(i, v + 0.1, f'{v:.2f}', ha='center')
        else:
            data[indicator].plot(kind='line', marker='o', ax=ax)
        
        # Set title
        if not title:
            title = f"{indicator} 比較"
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        # Format y-axis if needed
        if any(kw in indicator.lower() for kw in ['率', 'roe', 'roa', '%']):
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
            
        # Adjust layout
        fig.tight_layout()
        
        return fig
    
    def create_dashboard(self, 
                       data: Dict[str, pd.Series],
                       company_name: str = "") -> plt.Figure:
        """
        Create a dashboard with multiple financial indicators.
        
        Parameters
        ----------
        data : Dict[str, pd.Series]
            Dictionary of indicator name to time series data
        company_name : str, optional
            Company name for the title
            
        Returns
        -------
        plt.Figure
            The matplotlib figure object containing all subplots
        """
        n_indicators = len(data)
        
        # Calculate grid dimensions
        if n_indicators <= 2:
            rows, cols = 1, n_indicators
        elif n_indicators <= 4:
            rows, cols = 2, 2
        else:
            rows = (n_indicators + 2) // 3  # Ceiling division
            cols = 3
            
        # Create figure and axes
        fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*4))
        
        # Make axes iterable even for single subplot
        if n_indicators == 1:
            axes = np.array([axes])
        
        # Flatten axes array for easy iteration
        if rows > 1 or cols > 1:
            axes_flat = axes.flatten()
        else:
            axes_flat = axes
        
        # Plot each indicator
        for i, (indicator_name, series) in enumerate(data.items()):
            if i < len(axes_flat):
                ax = axes_flat[i]
                
                # Plot the data
                ax.plot(series.index, series.values, marker='o')
                
                # Set title and labels
                ax.set_title(indicator_name)
                ax.set_xlabel("日期")
                
                # Format y-axis if appropriate
                if any(kw in indicator_name.lower() for kw in ['率', 'roe', 'roa', '%']):
                    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
                
                # Add grid
                ax.grid(True, alpha=0.3)
        
        # Hide unused subplots
        for j in range(i+1, len(axes_flat)):
            axes_flat[j].axis('off')
        
        # Add overall title
        if company_name:
            fig.suptitle(f"{company_name} 財務指標摘要", fontsize=16, fontweight='bold')
            
        # Adjust layout
        fig.tight_layout()
        if company_name:
            fig.subplots_adjust(top=0.9)  # Make room for suptitle
            
        return fig


def plot_indicator(df: pd.DataFrame, 
                  indicator_series: pd.Series, 
                  title: str) -> plt.Figure:
    """
    Plot a single indicator time series.
    
    This is a convenience wrapper around FinancialPlotter.plot_indicator_trend
    for backward compatibility.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing time information
    indicator_series : pd.Series
        Series of indicator values
    title : str
        Plot title
        
    Returns
    -------
    plt.Figure
        The matplotlib figure object
    """
    plotter = FinancialPlotter()
    
    # Create a Series with the appropriate index
    if "Year" in df.columns:
        series = pd.Series(indicator_series.values, index=df["Year"])
    else:
        # Use default numeric index
        series = indicator_series
        
    return plotter.plot_indicator_trend(series, title)


def plot_trends(company_id: str = None, indicators: List[str] = None) -> plt.Figure:
    """
    Plot financial trends for specified company and indicators.
    
    Parameters
    ----------
    company_id : str, optional
        Company ID to analyze
    indicators : List[str], optional
        List of indicators to plot
        
    Returns
    -------
    plt.Figure
        The matplotlib figure with trend plots
    """
    # This is a stub implementation for the Streamlit app
    # In a real application, this would load data and create visualizations
    
    # Create a sample figure for demonstration
    plotter = FinancialPlotter()
    
    # Create sample data
    years = pd.date_range(start='2018-01-01', periods=5, freq='Y')
    
    if not indicators:
        indicators = ["ROE", "ROA", "營業利益率", "淨利率"]
    
    data = {}
    for indicator in indicators:
        # Generate random data with an upward trend and some noise
        base = np.linspace(5, 15, len(years))
        noise = np.random.normal(0, 1, len(years))
        values = base + noise
        data[indicator] = pd.Series(values, index=years)
    
    company_name = company_id if company_id else "範例公司"
    
    return plotter.create_dashboard(data, company_name)


if __name__ == "__main__":
    # Example usage
    plotter = FinancialPlotter()
    
    # Sample data
    years = pd.date_range(start='2018-01-01', periods=5, freq='Y')
    roe_values = [10.2, 11.5, 9.8, 12.3, 13.5]
    roe_series = pd.Series(roe_values, index=years)
    
    # Plot single indicator
    fig = plotter.plot_indicator_trend(roe_series, "ROE", "範例公司", include_avg=True)
    
    # Save or display
    plt.show()