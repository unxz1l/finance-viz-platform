import streamlit as st
import pandas as pd
from finance_analyzer.data.loader import DataLoader
from finance_analyzer.visualization.plotter import FinancialPlotter
from finance_analyzer.analysis.insights import FinancialInsights

# Page configuration
st.set_page_config(
    page_title="財務指標分析",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 財務指標分析平台")

# Sidebar for company selection
with st.sidebar:
    st.header("公司選擇")
    companies = st.multiselect(
        "選擇公司（可複選）",
        options=DataLoader.get_available_companies(),
        default=None
    )

# Main content
if companies:
    # Create tabs for different views
    tab1, tab2 = st.tabs(["趨勢分析", "年度比較"])
    
    with tab1:
        st.header("財務指標趨勢")
        
        # Metric selection
        metric = st.selectbox(
            "選擇指標",
            options=['ROE', 'Revenue Growth', 'Operating Margin Growth'],
            index=0
        )
        
        # Create and display plots for each selected company
        for company in companies:
            df = DataLoader.load_company_data(company)
            if df is not None and not df.empty:
                fig = FinancialPlotter.create_metric_line_chart(df, metric)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("年度比較")
        
        # Year selection
        year = st.selectbox(
            "選擇年度",
            options=[str(y) for y in range(103, 114)],  # 103-113年
            index=0
        )
        
        # Create comparison tables for each selected company
        for company in companies:
            df = DataLoader.load_company_data(company)
            if df is not None and not df.empty:
                st.subheader(company)
                comparison = FinancialPlotter.create_comparison_table(df, year)
                if not comparison.empty:
                    st.table(comparison)
                    
                    # Simple risk assessment
                    st.write("投資風險評估：")
                    risk_assessment = FinancialInsights.assess_risk(df)
                    for metric, assessment in risk_assessment.items():
                        if "良好" in assessment or "強勁" in assessment:
                            st.success(assessment)
                        else:
                            st.warning(assessment)
else:
    st.info("請從側邊欄選擇公司")