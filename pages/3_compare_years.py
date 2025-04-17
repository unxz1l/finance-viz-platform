import streamlit as st
from modules.insights import generate_insights

st.title("🧠 雙期比較與自動判讀")

company = st.selectbox("公司", ["王品", "乾杯", "八方雲集"])
year = st.selectbox("基準年度", [2022, 2021, 2020])  # 自訂
insights = generate_insights(company, year)

st.write("判讀結果：")
st.markdown(insights)