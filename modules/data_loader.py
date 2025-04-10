import pandas as pd

def load_financial_data(company_name: str) -> pd.DataFrame:
    path = f"data/{company_name.lower()}.csv"
    df = pd.read_csv(path)
    return df