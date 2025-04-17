import streamlit as st
from modules.visualizer import plot_trends

st.title("📈 財務指標趨勢")
# 可加入多公司選擇、年份區間等
plot_trends()