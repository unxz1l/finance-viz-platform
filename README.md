# Financial Indicator Visualization Platform

A Streamlit-based application that helps non-professional investors visualize and understand the key financial indicators of Taiwanese public companies.

本平台使用 Streamlit 製作，協助非專業投資人快速理解台灣上市櫃公司之財務指標與投資風險。

> Developed as a course project for *Introduction to Programming* (Course Code 11320QF100300)  
> Department of Quantitative Finance, National Tsing Hua University  
> Instructor: Prof. Cheng-Chi Chen 陳政琦

## Current Status

- **Supported Companies**: Currently supporting 9 restaurant companies:
  - TWSE Listed (上市):
    - 2727 王品股份有限公司
    - 2729 瓦城泰統股份有限公司
    - 2753 八方雲集國際股份有限公司
    - 7705 三商餐飲股份有限公司
  - TPEx Listed (上櫃):
    - 1259 安心食品服務股份有限公司
    - 1268 漢來美食股份有限公司
    - 7708 全家國際餐飲股份有限公司
    - 2752 豆府股份有限公司
    - 4419 皇家國際美食股份有限公司

- **Data Sources**:
  - TWSE Open API: https://openapi.twse.com.tw
  - TPEx Open API: https://www.tpex.org.tw/openapi

## Features

- **Company Selection**: Quick selection of companies via dropdown menu
- **Financial Metrics Dashboard**: Real-time display of core financial metrics
- **Interactive Trend Analysis**: Interactive charts with multiple metric support
- **Automated Insights**: Automatic generation of financial insights
- **Data Caching**: Intelligent data caching for improved performance

## Technical Stack

- Python 3.9+
- Streamlit (UI)
- Pandas / NumPy (data processing)
- Plotly (visualization)
- Requests (data fetching)
- Data Source: Taiwan Stock Exchange (TWSE) and Taipei Exchange (TPEx) APIs

## Project Structure

```
finance-viz-platform/
├── README.md                  # Documentation
├── requirements.txt           # Dependencies
├── .gitignore                # Git ignore file
├── finance_analyzer/         # Core analysis module
│   ├── __init__.py
│   ├── analysis/            # Financial analysis
│   │   ├── __init__.py
│   │   └── indicators.py    # Financial indicators calculation
│   ├── data/               # Data processing
│   │   ├── __init__.py
│   │   ├── loader.py       # TWSE/TPEx data loading and caching
│   │   └── processor.py    # Data preprocessing and transformation
│   └── visualization/      # Visualization
│       ├── __init__.py
│       └── plotter.py      # Interactive chart generation
├── app/                    # Application interface
│   ├── __init__.py
│   └── app.py             # Streamlit main application
└── test/                  # Test suite
    ├── __init__.py
    ├── test_data_loader.py
    └── test_twse_api.py
```

## Core Financial Metrics

1. **Return on Equity (ROE)**
   - Measures efficiency of capital utilization
   - Higher ROE indicates better capital efficiency

2. **Operating Margin**
   - Measures core business profitability
   - Reflects efficiency in converting revenue to profit

3. **Debt Ratio**
   - Evaluates financial leverage
   - Helps assess financial risk

4. **Revenue Growth**
   - Measures business expansion rate
   - Consistent growth indicates stable business development

## Data Management

The application uses a cache system to store API responses:

- Cache Location: User's system cache directory
  - macOS: `~/Library/Caches/finance-viz-platform`
  - Linux: `~/.cache/finance-viz-platform`
  - Windows: `%LOCALAPPDATA%\finance-viz-platform\Cache`

- Cache Files:
  - `twse_is_YYYYMMDD.csv`: TWSE market data
  - `tpex_is_YYYYMMDD.csv`: TPEx market data

The cache is automatically managed by the system and can be safely deleted if needed.

## Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/finance-viz-platform.git

# Navigate to project directory
cd finance-viz-platform

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Method 1: Using run script (Recommended)
chmod +x run.sh  # Make the script executable
./run.sh         # This will set up everything and run the app

# Method 2: Manual setup
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the application
streamlit run app/app.py
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=finance_analyzer tests/

# Run specific test file
pytest tests/test_data_loader.py
```

### Code Style

This project follows the PEP 8 style guide. We use:
- `black` for code formatting
- `flake8` for style guide enforcement
- `mypy` for type checking
- `isort` for import sorting

```bash
# Format code
black .

# Check style
flake8 .

# Sort imports
isort .

# Type checking
mypy .
```

## Usage Guide

1. **Company Selection**
   - Select company from sidebar dropdown
   - Companies are grouped by market (TWSE/TPEx)

2. **Financial Metrics**
   - View real-time core financial metrics
   - Includes ROE, Operating Margin, Debt Ratio
   - Data is automatically cached for performance

3. **Trend Analysis**
   - Switch between different financial metrics
   - View historical trends
   - Interactive chart features

4. **Detailed Data**
   - View complete financial data table
   - All data displayed in percentage format
   - Export data functionality available

## Contributing

Contributions are welcome. Please ensure:

1. Follow existing code style (use `black` and `flake8`)
2. Add appropriate tests (maintain test coverage)
3. Update documentation as needed
4. Create a pull request with a clear description

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Taiwan Stock Exchange (TWSE) for providing financial data API
- Taipei Exchange (TPEx) for providing OTC market data API
- Streamlit team for the excellent web framework
