import streamlit as st
import os
from modules.data_loader import load_company_list

st.title("🔍 選擇公司與年度")

company_options = load_company_list()
company = st.selectbox("選擇公司", company_options)
year = st.selectbox("選擇年度", list(range(2013, 2024)))

st.write(f"你選擇的是：{company}（{year} 年）")