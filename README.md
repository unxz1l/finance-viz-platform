# Financial Indicator Visualization Platform

A Streamlit-based application that helps non-professional investors visualize and understand the key financial indicators of Taiwanese public companies.

本平台使用 Streamlit 製作，協助非專業投資人快速理解台灣上市櫃公司之財務指標與投資風險。

Developed as a course project for Introduction to Programming (Course Code 11320QF100300)
Department of Quantitative Finance, National Tsing Hua University
Instructor: Prof. Cheng-Chi Chen 陳政琦

## Current Status

### Supported Companies
Currently supporting 11 restaurant companies:

**TWSE 上市公司：**
- 2727 王品股份有限公司
- 2753 八方雲集國際股份有限公司
- 2723 美食-KY股份有限公司

**TPEx 上櫃公司：**
- 2729 瓦城泰統股份有限公司
- 2732 六角國際事業股份有限公司
- 1259 安心食品服務股份有限公司
- 1268 漢來美食股份有限公司
- 2752 豆府股份有限公司
- 4419 皇家美食股份有限公司

### Data Sources
- TWSE Open API: https://openapi.twse.com.tw
- TPEx Open API: https://www.tpex.org.tw/openapi

## Features

### Company Selection
- Quick selection of companies via dropdown menu
- Support for multiple company comparison

### Financial Metrics Dashboard
- Real-time display of core financial metrics
- Key indicators:
  - Return on Equity (ROE)
  - Revenue Growth Rate
  - Operating Margin Growth Rate

### Interactive Analysis
- Interactive trend charts with multiple metric support
- Year-over-year comparison tables
- Simple investment risk assessment

### Technical Features
- Intelligent data caching for improved performance
- Responsive UI design
- Chinese/English bilingual support

## Technical Stack

### Core Dependencies
- Python 3.9+
- Streamlit (UI)
- Pandas / NumPy (data processing)
- Plotly (visualization)
- Requests (data fetching)

### Data Sources
- Taiwan Stock Exchange (TWSE) API
- Taipei Exchange (TPEx) API

## Project Structure

```
finance-viz-platform/
├── README.md                  # Documentation
├── requirements.txt           # Core dependencies
├── requirements-dev.txt       # Development dependencies
├── .gitignore                # Git ignore file
├── finance_analyzer/         # Core analysis module
│   ├── __init__.py
│   ├── analysis/            # Financial analysis
│   │   ├── indicators.py    # Financial indicators calculation
│   │   └── insights.py      # Financial insights generation
│   ├── data/               # Data processing
│   │   ├── __init__.py
│   │   ├── loader.py       # Data loading and caching
│   │   └── processor.py    # Data processing utilities
│   └── visualization/      # Visualization
│       ├── __init__.py
│       ├── plotter.py      # Chart generation
│       └── dashboard.py    # Dashboard components
├── app/                    # Application interface
│   ├── __init__.py
│   └── app.py             # Main application
└── test/                  # Test suite
    ├── test_data_loader.py    # Data loader tests
    ├── test_visualization.py  # Visualization tests
    ├── test_indicators.py     # Financial indicators tests
    └── test_twse_api.py       # API integration tests
```

## Installation

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (for testing and development)
pip install -r requirements-dev.txt

# Run the application
streamlit run app/app.py

# Run tests
pytest test/
```

## Usage

1. Select companies from the dropdown menu
2. View financial indicator trends
3. Compare annual performance
4. Review investment risk assessment

## Core Financial Metrics

### Return on Equity (ROE)
- Definition: Net Income / Shareholders' Equity
- Purpose: Measures company's profitability relative to shareholders' equity
- Interpretation: Higher ROE indicates better profitability

### Revenue Growth Rate
- Definition: (Current Revenue - Previous Revenue) / Previous Revenue
- Purpose: Measures company's revenue growth
- Interpretation: Positive growth indicates business expansion

### Operating Margin Growth Rate
- Definition: (Current Operating Margin - Previous Operating Margin) / Previous Operating Margin
- Purpose: Measures company's operational efficiency improvement
- Interpretation: Positive growth indicates improving operational efficiency
