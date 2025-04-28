# Financial Indicator Visualization Platform

A Streamlit-based application that helps non-professional investors visualize and understand the key financial indicators of Taiwanese public companies.

本平台使用 Streamlit 製作，協助非專業投資人快速理解台灣上市櫃公司之財務指標與投資風險。

> Developed as a course project for *Introduction to Programming* (Course Code 11320QF100300)  
> Department of Quantitative Finance, National Tsing Hua University  
> Instructor: Prof. Cheng-Chi Chen 陳政琦

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
- Data Source: Taiwan Stock Exchange (TWSE) financial statements

## Project Structure

```
finance-viz-platform/
├── README.md                  # Documentation
├── requirements.txt           # Dependencies
├── .gitignore                 # Git ignore file
├── finance_analyzer/          # Core analysis module
│   ├── __init__.py
│   ├── analysis/              # Financial analysis
│   │   ├── __init__.py
│   │   ├── analyzer.py        # Core financial metrics analysis
│   │   └── insights.py        # Financial insights generation
│   ├── data/                  # Data processing
│   │   ├── __init__.py
│   │   ├── loader.py          # TWSE data loading and caching
│   │   └── processor.py       # Data preprocessing and transformation
│   └── visualization/         # Visualization
│       ├── __init__.py
│       └── plotter.py         # Interactive chart generation
└── app/                       # Application interface
    ├── __init__.py
    └── app.py                 # Streamlit main application
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
pip install -r requirements.txt
pip install -e .
export PYTHONPATH=$PYTHONPATH:$(pwd)  # Set PYTHONPATH
streamlit run app/app.py
```

## Usage Guide

1. **Company Selection**
   - Select company from sidebar dropdown

2. **Financial Metrics**
   - View real-time core financial metrics
   - Includes ROE, Operating Margin, Debt Ratio

3. **Trend Analysis**
   - Switch between different financial metrics
   - View historical trends
   - Interactive chart features

4. **Detailed Data**
   - View complete financial data table
   - All data displayed in percentage format

## Contributing

Contributions are welcome. Please ensure:

1. Follow existing code style
2. Update relevant documentation
3. Add appropriate tests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
