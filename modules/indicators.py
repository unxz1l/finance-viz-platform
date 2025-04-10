def calculate_roe(df):
    return df["Net Income"] / df["Shareholder Equity"]

def calculate_revenue_growth(df):
    return df["Revenue"].pct_change()

def calculate_operating_income_growth(df):
    return df["Operating Income"].pct_change()

def calculate_rnd_to_revenue(df):
    return df["R&D Expense"] / df["Revenue"]