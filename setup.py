from setuptools import setup, find_packages

setup(
    name="finance_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "requests>=2.31.0",
        "plotly>=5.19.0",
        "python-dateutil>=2.9.0",
        "pytz>=2025.2",
        "toml>=0.10.2",
        "altair>=5.5.0,<6.0.0",
        "pillow>=11.2.0,<12.0.0",
    ],
) 