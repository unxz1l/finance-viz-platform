#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Set PYTHONPATH to include the project root
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Install the package in development mode
pip install -e .

# Run the Streamlit app
streamlit run app/app.py 