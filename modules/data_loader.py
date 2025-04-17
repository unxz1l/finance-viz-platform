import pandas as pd
import os

def load_company_list():
    # 從資料夾中抓公司清單
    files = os.listdir("data/")
    return [f.split(".")[0] for f in files if f.endswith(".csv")]

def load_financial_data(company: str):
    df = pd.read_csv(f"data/{company}.csv")
    return df