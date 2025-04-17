import pandas as pd

def calc_roe(df_bs:pd.DataFrame, df_is:pd.DataFrame):
    equity = df_bs["權益總額"]
    net    = df_is["本期淨利（損）"]
    # 用去年同期 + 今年同期平均，簡化版
    roe = net / (equity.rolling(2).mean()) * 100
    return roe.round(2)

def yoy_growth(current:pd.Series, previous:pd.Series):
    return ((current - previous) / previous * 100).round(2)