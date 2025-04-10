import streamlit as st
from modules.data_loader import load_financial_data
from modules.indicators import calculate_roe
from modules.visualizer import plot_indicator

st.title("財務指標視覺化平台")

company = st.selectbox("選擇公司", ["王品", "八方雲集"])
df = load_financial_data(company)

roe = calculate_roe(df)
fig = plot_indicator(df, roe, "ROE")
st.pyplot(fig)