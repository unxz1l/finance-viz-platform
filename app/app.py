import streamlit as st
import pandas as pd
import plotly.express as px
from finance_analyzer.data.loader import DataLoader

# Page configuration
st.set_page_config(
    page_title="財務數據分析",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 財務數據分析平台")

# Sidebar for company selection
with st.sidebar:
    st.header("公司選擇")
    company = st.selectbox(
        "選擇公司",
        options=DataLoader.get_available_companies(),
        index=0
    )

# Main content
if company:
    # Load company data
    df = DataLoader.load_company_data(company)
    
    if df is not None and not df.empty:
        # Display basic metrics
        st.header(f"{company} 財務指標")
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("ROE", f"{df['ROE'].iloc[-1]:.1%}")
        with col2:
            st.metric("營業淨利率", f"{df['Operating_Margin'].iloc[-1]:.1%}")
        with col3:
            st.metric("負債比率", f"{df['Debt_Ratio'].iloc[-1]:.1%}")
        
        # Plot trends
        st.header("趨勢分析")
        
        # Metric selection
        metric = st.selectbox(
            "選擇指標",
            options=['ROE', 'Operating_Margin', 'Debt_Ratio', 'Revenue_Growth'],
            index=0
        )
        
        # Create and display plot
        fig = px.line(
            df,
            x='year',
            y=metric,
            title=f"{metric} 趨勢",
            markers=True
        )
        fig.update_layout(
            xaxis_title="年度",
            yaxis_title=metric,
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table
        st.header("詳細數據")
        st.dataframe(df.style.format({
            'ROE': '{:.1%}',
            'Operating_Margin': '{:.1%}',
            'Debt_Ratio': '{:.1%}',
            'Revenue_Growth': '{:.1%}'
        }))
    else:
        st.error("無法載入公司數據")
else:
    st.info("請從側邊欄選擇公司")