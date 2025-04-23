import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Finance Visualization Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title and description
st.title("📊 Finance Visualization Platform")
st.markdown("""
Welcome to the Finance Visualization Platform! This platform provides comprehensive tools for:
- Market analysis and visualization
- Portfolio tracking and analysis
- Company-specific financial metrics
- Risk assessment and management
""")

# Navigation cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 Market Overview")
    st.markdown("""
    - Real-time market indices
    - Sector performance analysis
    - Market trends and patterns
    """)
    st.page_link("pages/dashboard.py", label="Go to Dashboard →")

with col2:
    st.markdown("### 💼 Portfolio Analysis")
    st.markdown("""
    - Portfolio performance tracking
    - Asset allocation visualization
    - Historical performance analysis
    """)
    st.page_link("pages/dashboard.py", label="Go to Dashboard →")

with col3:
    st.markdown("### 🏢 Company Analysis")
    st.markdown("""
    - Company financial metrics
    - Stock performance analysis
    - Fundamental analysis tools
    """)
    st.page_link("pages/company_analysis.py", label="Go to Company Analysis →")

# Footer
st.markdown("---")
st.markdown("© 2024 Finance Visualization Platform")