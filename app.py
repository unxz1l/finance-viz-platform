import streamlit as st
from modules.data_loader import load_financial_data
from modules.indicators import calculate_roe
from modules.visualizer import plot_indicator

# app.py
import streamlit as st

st.set_page_config(page_title="財務視覺化平台", layout="wide")

st.title("📊 財務指標視覺化平台")
st.markdown("""
歡迎使用本平台，我們提供簡單直觀的方式，幫助您理解一家公司的財務健康狀況與投資風險。

請從左側選單選擇頁面開始操作。
""")

company = st.selectbox("選擇公司", ["王品", "八方雲集"])
df = load_financial_data(company)

roe = calculate_roe(df)
fig = plot_indicator(df, roe, "ROE")
st.pyplot(fig)