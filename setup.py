from setuptools import setup, find_packages

setup(
    name="finance_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "streamlit",
        "requests",
        "lxml",
        "html5lib",
        "numpy",
        "plotly",
    ],
    author="程設第五組",
    description="財務視覺化平台，幫助使用者快速理解公司的財務健康狀況與投資風險，提供互動式圖表與即時數據分析",
    keywords="finance, visualization, streamlit, taiwan stock, plotly",
    python_requires=">=3.8",
)