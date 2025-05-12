# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from finance_analyzer.data.loader import DataLoader as ExternalDataLoader

# 設置頁面配置
st.set_page_config(
    page_title="餐飲業財務分析儀表板",
    page_icon="🍽️",
    layout="wide"
)

# 添加自定義CSS
st.markdown("""
<style>
    .main {
        background-color: #FFF5F0;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #581845;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
    }
    .stButton>button:hover {
        background-color: #C70039;
    }
    .highlight {
        background-color: #FFF5F0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF5733;
    }
    .risk {
        background-color: #FFE5E5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #C70039;
        margin-bottom: 10px;
    }
    .opportunity {
        background-color: #E5FFE5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 定義財務數據處理類
class FinancialData:
    def __init__(self):
        # 讀取CSV文件
        try:
            self.df = pd.read_csv('output/selected_companies_financials.csv')
            # 確保年份列是整數類型
            self.df['年份'] = self.df['年份'].astype(int)
            # 確保公司代碼是字符串類型
            self.df['公司代號'] = self.df['公司代號'].astype(str)
        except Exception as e:
            st.error(f"數據讀取錯誤: {str(e)}")
            self.df = pd.DataFrame()
        
        # 建立公司代碼與名稱的對應
        self.company_names = {
            "2723": "美食-KY",
            "2727": "王品",
            "2729": "瓦城",
            "2732": "六角",
            "1268": "漢來美食"
        }
        
        # 定義指標名稱對應
        self.metric_names = {
            "debt_ratio": "財務結構-負債佔資產比率(%)",
            "long_term_funds_to_fixed_assets": "財務結構-長期資金佔不動產、廠房及設備比率(%)",
            "current_ratio": "償債能力-流動比率(%)",
            "quick_ratio": "償債能力-速動比率(%)",
            "interest_coverage": "償債能力-利息保障倍數(%)",
            "receivable_turnover": "經營能力-應收款項週轉率(次)",
            "average_collection_days": "經營能力-平均收現日數",
            "inventory_turnover": "經營能力-存貨週轉率(次)",
            "average_days_sales": "經營能力-平均售貨日數",
            "fixed_asset_turnover": "經營能力-不動產、廠房及設備週轉率(次)",
            "asset_turnover": "經營能力-總資產週轉率(次)",
            "roa": "獲利能力-資產報酬率(%)",
            "roe": "獲利能力-權益報酬率(%)",
            "pretax_profit_to_paidin_capital": "獲利能力-稅前純益佔實收資本比率(%)",
            "profit_margin": "獲利能力-純益率(%)",
            "eps": "獲利能力-每股盈餘(元)",
            "cash_flow_ratio": "現金流量-現金流量比率(%)",
            "cash_flow_adequacy": "現金流量-現金流量允當比率(%)",
            "reinvestment_ratio": "現金流量-現金再投<br>資比率(%)"
        }
        
        # 初始化風險與亮點分析數據
        self.risk_highlight_data = {
            "美食-KY": {
                "111": {
                    "risks": [
                        "原物料成本上升壓縮利潤",
                        "資金成本上升風險",
                        "市場競爭加劇"
                    ],
                    "highlights": [
                        "新產品線帶動銷售增長",
                        "數位行銷策略成效顯著",
                        "成本控制優化"
                    ]
                },
                "113": {
                    "risks": [
                        "消費者偏好快速變化",
                        "國際擴張不確定性",
                        "食品安全風險"
                    ],
                    "highlights": [
                        "高端市場領導地位鞏固",
                        "數位轉型成效顯著",
                        "ESG策略獲得正面評價"
                    ]
                }
            }
        }

    def get_company_names(self):
        """獲取所有公司名稱"""
        return list(self.company_names.values())

    def get_company_code(self, company_name):
        """獲取公司代碼"""
        for code, name in self.company_names.items():
            if name == company_name:
                return code
        return None

    def get_years(self):
        """獲取所有年度"""
        return sorted(self.df['年份'].unique().astype(str))
    
    def get_metric_names(self):
        """獲取所有指標名稱"""
        return self.metric_names
    
    def get_data_for_years(self, company_name, metric, years_range):
        """獲取特定年份範圍的數據"""
        try:
            code = self.get_company_code(company_name)
            if code is None:
                st.error(f"找不到公司代碼: {company_name}")
                return {}
            
            company_data = self.df[self.df['公司代號'] == code].copy()
            
            if company_data.empty:
                st.error(f"找不到公司數據: {company_name}")
                return {}
            
            # 獲取公司實際有的年份
            available_years = sorted(company_data['年份'].unique())
            
            if years_range == 5:
                selected_years = available_years[-5:] if len(available_years) >= 5 else available_years
            else:  # 10年
                selected_years = available_years[-10:] if len(available_years) >= 10 else available_years
            
            company_data = company_data[company_data['年份'].isin(selected_years)]
            
            if metric not in company_data.columns:
                st.error(f"找不到指標: {metric}")
                return {}
            
            # 確保年份是字符串格式，並且只返回存在的年份的數據
            return {str(year): float(value) for year, value in zip(company_data['年份'], company_data[metric])}
            
        except Exception as e:
            st.error(f"數據處理錯誤: {str(e)}")
            return {}

    def get_risk_highlight(self, company_name, year):
        code = self.get_company_code(company_name)
        year_str = str(year)
        info = self.risk_highlight_data.get(company_name, {}).get(year_str, {})
        risks = info.get('risks', [])
        highlights = info.get('highlights', [])
        return risks, highlights

# 圖表生成器類
class ChartGenerator:
    def __init__(self, financial_data):
        self.financial_data = financial_data

    def generate_line_chart(self, selected_companies, metric, years_range):
        """生成折線圖"""
        try:
            fig = go.Figure()
            
            for company in selected_companies:
                data = self.financial_data.get_data_for_years(company, metric, years_range)
                if not data:
                    continue
                    
                years = list(data.keys())
                values = list(data.values())
                
                fig.add_trace(go.Scatter(
                    x=years,
                    y=values,
                    mode='lines+markers',
                    name=company,
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title=f"{metric} 趨勢圖",
                xaxis_title="年度",
                yaxis_title=metric,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=40, r=40, t=60, b=40),
                template="seaborn",
                height=500
            )
            
            return fig
            
        except Exception as e:
            st.error(f"圖表生成錯誤: {str(e)}")
            return go.Figure()

    def generate_comparison_table(self, company_name, year):
        """生成比較表格"""
        code = self.financial_data.get_company_code(company_name)
        company_data = self.financial_data.df[self.financial_data.df['公司代號'] == code].copy()
        
        # 獲取可用的年份
        available_years = sorted(company_data['年份'].unique())
        if year not in available_years:
            st.warning(f"找不到 {year} 年的數據")
            return pd.DataFrame(), None
            
        prev_year = year - 1
        if prev_year not in available_years:
            st.warning(f"找不到 {prev_year} 年的數據")
            return pd.DataFrame(), None
            
        data = []
        for metric in self.financial_data.get_metric_names():
            name = self.financial_data.get_metric_names()[metric]
            try:
                current_value = float(company_data[company_data['年份'] == year][name].values[0])
                prev_value = float(company_data[company_data['年份'] == prev_year][name].values[0])
                change = current_value - prev_value
                change_percent = (change / prev_value * 100) if prev_value != 0 else 0
                change_direction = "↑" if change > 0 else "↓"
                
                data.append({
                    "財務指標": name,
                    f"{year}年": f"{current_value:.2f}",
                    f"{prev_year}年": f"{prev_value:.2f}",
                    "變化": f"{change_direction} {abs(change):.2f} ({abs(change_percent):.2f}%)"
                })
            except (ValueError, TypeError):
                # 如果無法轉換為數值，則跳過該指標
                continue
        
        return pd.DataFrame(data), prev_year

# Streamlit App 類
class FinancialAnalysisApp:
    def __init__(self):
        self.financial_data = FinancialData()
        self.chart_generator = ChartGenerator(self.financial_data)

    def run(self):
        st.markdown("<h1 style='text-align: center; color: #581845;'>餐飲業財務分析儀表板</h1>", unsafe_allow_html=True)
        
        st.sidebar.markdown("### 選擇分析參數")
        
        # 公司多選
        selected_companies = st.sidebar.multiselect(
            "選擇感興趣的公司",
            self.financial_data.get_company_names(),
            default=[self.financial_data.get_company_names()[0]]
        )
        
        # 時間範圍選擇
        years_range = st.sidebar.radio(
            "選擇時間範圍",
            [5, 10],
            format_func=lambda x: f"近{x}年"
        )
        
        # 財務指標選擇
        selected_metric = st.sidebar.selectbox(
            "選擇財務指標",
            [
                "財務結構-負債佔資產比率(%)",
                "獲利能力-純益率(%)",
                "獲利能力-權益報酬率(%)",
                "獲利能力-每股盈餘(元)",
                "現金流量-現金流量比率(%)"
            ]
        )

        if not selected_companies:
            st.warning("請至少選擇一家要比較的公司！")
            return

        # 生成並顯示圖表
        fig = self.chart_generator.generate_line_chart(selected_companies, selected_metric, years_range)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("無法生成圖表，請檢查數據源")
            return
        
        # 分隔線
        st.markdown("---")
        
        # 詳細分析區域
        st.markdown("### 詳細財務分析")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 公司選擇
            company_for_detail = st.selectbox(
                "選擇公司",
                selected_companies,
                key="company_detail"
            )
        
        with col2:
            # 年度選擇
            available_years = self.financial_data.get_years()
            if years_range == 5:
                display_years = available_years[-5:]
            else:
                display_years = available_years[-10:]
            
            selected_year = st.selectbox(
                "選擇年度",
                display_years,
                index=len(display_years)-1,
                format_func=lambda x: f"{x}年",
                key="year_detail"
            )
        
        # 生成比較表格
        df, prev_year = self.chart_generator.generate_comparison_table(company_for_detail, int(selected_year))
        
        if not df.empty:
            st.markdown(f"#### {company_for_detail} ({self.financial_data.get_company_code(company_for_detail)}) {selected_year}年 vs {prev_year}年 財務比較")
            
            # 顯示表格
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            # 風險與亮點分析
            st.markdown("#### 投資風險與亮點分析")
            
            risks, highlights = self.financial_data.get_risk_highlight(company_for_detail, selected_year)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="risk">', unsafe_allow_html=True)
                st.markdown("##### 潛在風險")
                for risk in risks:
                    st.markdown(f"- {risk}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="opportunity">', unsafe_allow_html=True)
                st.markdown("##### 投資亮點")
                for highlight in highlights:
                    st.markdown(f"- {highlight}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("無法生成比較表格，請檢查數據源")

# 執行應用程序
if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.run() 