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

# 資料加載器類
class DataLoader:
    """從外部源加載財務數據"""
    
    def __init__(self):
        self.external_loader = ExternalDataLoader()
    
    def load_company_list(self):
        """加載公司列表"""
        try:
            # 使用外部數據加載器的公司列表
            companies = {}
            for company in self.external_loader.COMPANIES:
                companies[company["name"]] = company["code"]
            return companies
        except Exception as e:
            st.error(f"加載公司列表時出錯: {e}")
            return {}
    
    def load_financial_data(self, company_name, company_code):
        """加載公司財務數據"""
        try:
            # 使用外部數據加載器獲取財務數據
            data = self.external_loader.load_company_data(f"{company_code} {company_name}")
            if data is None:
                st.warning(f"無法獲取 {company_name} 的財務數據")
                return pd.DataFrame()
            
            # 創建一個空的 DataFrame 來存儲財務數據
            years = [str(year) for year in range(103, 114)]  # 103-113年
            financial_data = pd.DataFrame(index=years, columns=[
                "revenue_growth",
                "profit_margin",
                "roe",
                "debt_ratio",
                "eps"
            ])
            
            # 從 API 數據中提取所需指標
            # 這裡我們使用一些示例數據，實際應用中應該從 API 返回的數據中提取
            for year in years:
                # 使用隨機數據作為示例
                financial_data.loc[year, "revenue_growth"] = round(np.random.uniform(-10, 30), 2)
                financial_data.loc[year, "profit_margin"] = round(np.random.uniform(5, 25), 2)
                financial_data.loc[year, "roe"] = round(np.random.uniform(5, 35), 2)
                financial_data.loc[year, "debt_ratio"] = round(np.random.uniform(20, 60), 2)
                financial_data.loc[year, "eps"] = round(np.random.uniform(1, 10), 2)
            
            return financial_data
            
        except Exception as e:
            st.error(f"加載財務數據時出錯: {e}")
            return pd.DataFrame()
    
    def load_risk_highlight_data(self, company_name, year):
        """加載風險與亮點數據"""
        try:
            # 使用外部數據加載器獲取風險與亮點數據
            data = self.external_loader.load_company_data(f"{company_name}")
            if data is None:
                return {"risks": ["無該年度風險資料"], "highlights": ["無該年度亮點資料"]}
            
            # 這裡需要根據實際API返回的數據結構進行調整
            return {
                    "risks": [
                    f"{company_name}的風險1 - 從外部數據來源",
                    f"{company_name}的風險2 - 從外部數據來源",
                    f"{company_name}的風險3 - 從外部數據來源"
                    ],
                    "highlights": [
                    f"{company_name}的亮點1 - 從外部數據來源",
                    f"{company_name}的亮點2 - 從外部數據來源",
                    f"{company_name}的亮點3 - 從外部數據來源"
                ]
            }
        except Exception as e:
            st.error(f"加載風險與亮點數據時出錯: {e}")
            return {"risks": ["數據加載錯誤"], "highlights": ["數據加載錯誤"]}
    
    def load_company_info(self, company_name):
        """加載公司基本信息"""
        try:
            # 保留模擬的公司信息
            company_info = {
                "王品股份有限公司": {
                    "full_name": "王品集團",
                    "industry": "連鎖餐飲",
                    "founded": "1993年",
                    "stores": "超過400家門市",
                    "description": "台灣知名連鎖餐飲集團，旗下擁有王品牛排、陶板屋、西堤、夏慕尼等多個品牌。"
                },
                "瓦城泰統股份有限公司": {
                    "full_name": "瓦城泰統集團",
                    "industry": "連鎖餐飲",
                    "founded": "1990年",
                    "stores": "超過100家門市",
                    "description": "以泰式料理起家，旗下擁有瓦城、非常泰、1010湘、十食湘、時時香、YABI等多個品牌。"
                },
                "八方雲集國際股份有限公司": {
                    "full_name": "八方雲集",
                    "industry": "連鎖餐飲",
                    "founded": "1998年",
                    "stores": "超過1,000家門市",
                    "description": "以平價美食聞名，主打鍋貼、水餃等中式點心，在台灣、中國、美國等地均有據點。"
                },
                "安心食品服務股份有限公司": {
                    "full_name": "安心食品",
                    "industry": "連鎖餐飲",
                    "founded": "1996年",
                    "stores": "超過200家門市",
                    "description": "以平價美食聞名，旗下擁有多個中式、日式、西式餐飲品牌，主打年輕消費族群。"
                },
                "漢來美食股份有限公司": {
                    "full_name": "漢來美食",
                    "industry": "連鎖餐飲",
                    "founded": "1995年",
                    "stores": "超過50家門市",
                    "description": "以高檔中餐起家，旗下擁有漢來海港、漢來蔬食等多個品牌，主打精緻餐飲服務。"
                },
                "全家國際餐飲股份有限公司": {
                    "full_name": "全家國際餐飲",
                    "industry": "連鎖餐飲",
                    "founded": "2000年",
                    "stores": "超過100家門市",
                    "description": "以日式料理為主，旗下擁有多個品牌，主打精緻日式餐飲服務。"
                },
                "三商餐飲股份有限公司": {
                    "full_name": "三商餐飲",
                    "industry": "連鎖餐飲",
                    "founded": "1992年",
                    "stores": "超過300家門市",
                    "description": "以平價美食聞名，旗下擁有多個品牌，主打年輕消費族群。"
                },
                "豆府股份有限公司": {
                    "full_name": "豆府",
                    "industry": "連鎖餐飲",
                    "founded": "2005年",
                    "stores": "超過50家門市",
                    "description": "以韓式料理為主，主打平價韓式美食，深受年輕族群喜愛。"
                },
                "皇家國際美食股份有限公司": {
                    "full_name": "皇家國際美食",
                    "industry": "連鎖餐飲",
                    "founded": "2008年",
                    "stores": "超過30家門市",
                    "description": "以高檔西式料理為主，主打精緻西式餐飲服務。"
                }
            }
            
            return company_info.get(company_name, {
                "full_name": company_name,
                "industry": "餐飲業",
                "founded": "未知",
                "stores": "未知",
                "description": f"{company_name}是一家餐飲業公司。"
            })
        except Exception as e:
            st.error(f"加載公司信息時出錯: {e}")
            return {}


# 圖表生成類
class ChartGenerator:
    def __init__(self):
        # 指標中文名稱對照
        self.metric_names = {
            "revenue_growth": "營收成長率 (%)",
            "profit_margin": "淨利率 (%)",
            "roe": "股東權益報酬率 (%)",
            "debt_ratio": "負債比率 (%)",
            "eps": "每股盈餘 (元)"
        }
    
    def generate_line_chart(self, selected_companies, metric, years_range):
        """生成折線圖"""
        companies_data = {}
        for company, code in selected_companies.items():
            # 從外部數據源加載數據
            df = DataLoader().load_financial_data(company, code)
            companies_data[company] = df
        
        if not companies_data:
            return None
        
        # 獲取年份範圍
        all_years = list(next(iter(companies_data.values())).index)
        if years_range == 5:
            selected_years = all_years[-5:]
        else:  # 10年
            selected_years = all_years[-10:]
        
        fig = go.Figure()
        
        for company, df in companies_data.items():
            if not df.empty:
                values = df.loc[selected_years, metric].values
                
                fig.add_trace(go.Scatter(
                    x=selected_years,
                    y=values,
                    mode='lines+markers',
                    name=f"{company} ({selected_companies[company]})",
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=f"{self.metric_names[metric]} 趨勢圖",
            xaxis_title="年度",
            yaxis_title=self.metric_names[metric],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            template="seaborn",
            height=500,
        )
        
        # 添加年度標籤
        fig.update_xaxes(
            ticktext=[f"{year}年" for year in selected_years],
            tickvals=selected_years
        )
        
        return fig
    
    def generate_comparison_table(self, company, company_code, year):
        """生成年度比較表格數據"""
        # 從外部數據源加載數據
        df = DataLoader().load_financial_data(company, company_code)
        
        if df.empty or year not in df.index:
            return []
        
        prev_year = str(int(year) - 1)
        if prev_year not in df.index:
            return []
        
        metrics = ["revenue_growth", "profit_margin", "roe", "debt_ratio", "eps"]
        
        comparison_data = []
        
        for metric in metrics:
            current_value = df.loc[year, metric]
            prev_value = df.loc[prev_year, metric]
            change = current_value - prev_value
            change_percent = (change / prev_value * 100) if prev_value != 0 else 0
            
            # 負債比率下降為正面
            if metric == "debt_ratio":
                change_direction = "↓" if change < 0 else "↑"
                change_class = "positive" if change < 0 else "negative"
            else:
                change_direction = "↑" if change > 0 else "↓"
                change_class = "positive" if change > 0 else "negative"
            
            comparison_data.append({
                "metric": self.metric_names[metric],
                "prev_value": round(prev_value, 2),
                "current_value": round(current_value, 2),
                "change": round(abs(change), 2),
                "change_percent": round(abs(change_percent), 2),
                "change_direction": change_direction,
                "change_class": change_class
            })
        
        return comparison_data, prev_year


# 應用程序類
class FinancialAnalysisApp:
    def __init__(self):
        self.chart_generator = ChartGenerator()
        self.data_loader = DataLoader()  # 初始化 DataLoader 實例
    
    def run(self):
        """運行應用程序"""
        st.markdown("<h1 style='text-align: center; color: #581845;'>餐飲業財務分析儀表板</h1>", unsafe_allow_html=True)
        
        # 加載公司列表
        companies = self.data_loader.load_company_list()  # 使用實例方法
        if not companies:
            st.error("無法加載公司列表")
            return
        
        # 側邊欄 - 公司選擇
        st.sidebar.markdown("### 選擇分析參數")
        
        # 公司多選
        selected_company_names = st.sidebar.multiselect(
            "選擇感興趣的公司",
            list(companies.keys()),
            default=[list(companies.keys())[0]]
        )
        
        # 創建選定公司的字典 {name: code}
        selected_companies = {name: companies[name] for name in selected_company_names if name in companies}
        
        # 時間範圍選擇
        years_range = st.sidebar.radio(
            "選擇時間範圍",
            [5, 10],
            format_func=lambda x: f"近{x}年"
        )
        
        # 財務指標選擇
        selected_metric = st.sidebar.selectbox(
            "選擇財務指標",
            ["revenue_growth", "profit_margin", "roe", "debt_ratio", "eps"],
            format_func=lambda x: self.chart_generator.metric_names[x]
        )
        
        # 主要內容區域
        if not selected_companies:
            st.warning("請至少選擇一家公司進行分析")
            return
        
        # 生成圖表
        st.markdown("### 財務指標趨勢圖")
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
                selected_company_names,
                key="company_detail"
            )
        
        with col2:
            # 年度選擇
            # 從外部數據源獲取年份列表
            df = self.data_loader.load_financial_data(company_for_detail, selected_companies[company_for_detail])  # 使用實例方法
            available_years = list(df.index)
            
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
        comparison_data, prev_year = self.chart_generator.generate_comparison_table(
            company_for_detail, 
            selected_companies[company_for_detail], 
            selected_year
        )
        
        if comparison_data:
            st.markdown(f"#### {company_for_detail} ({selected_companies[company_for_detail]}) {selected_year}年 vs {prev_year}年 財務比較")
            
            # 使用DataFrame顯示比較表格
            df = pd.DataFrame(comparison_data)
            
            # 格式化顯示
            formatted_df = pd.DataFrame({
                "財務指標": df["metric"],
                f"{prev_year}年": df["prev_value"],
                f"{selected_year}年": df["current_value"],
                "變化": [f"{row['change_direction']} {row['change']} ({row['change_percent']}%)" for _, row in df.iterrows()]
            })
            
            # 顯示表格
            st.dataframe(
                formatted_df,
                use_container_width=True,
                hide_index=True
            )
            
            # 風險與亮點分析
            st.markdown("#### 投資風險與亮點分析")
            
            risk_highlight = self.data_loader.load_risk_highlight_data(company_for_detail, selected_year)  # 使用實例方法
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="risk">', unsafe_allow_html=True)
                st.markdown("##### 潛在風險")
                for risk in risk_highlight["risks"]:
                    st.markdown(f"- {risk}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="opportunity">', unsafe_allow_html=True)
                st.markdown("##### 投資亮點")
                for highlight in risk_highlight["highlights"]:
                    st.markdown(f"- {highlight}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 公司基本資訊卡片
            st.markdown("#### 公司基本資訊")
            
            company_info = self.data_loader.load_company_info(company_for_detail)  # 使用實例方法
            
            if company_info:
                st.markdown(f"""
                <div class="highlight">
                    <h5>{company_for_detail} ({selected_companies[company_for_detail]}) - {company_info.get('full_name', '')}</h5>
                    <p><strong>產業類別:</strong> {company_info.get('industry', '')}</p>
                    <p><strong>成立時間:</strong> {company_info.get('founded', '')}</p>
                    <p><strong>門市規模:</strong> {company_info.get('stores', '')}</p>
                    <p><strong>公司簡介:</strong> {company_info.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("無法加載公司基本資訊")
        else:
            st.warning("無法生成比較表格，請檢查數據源")


# 執行應用程序
if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.run()