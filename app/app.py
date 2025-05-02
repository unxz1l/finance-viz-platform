# -*- coding: utf-8 -*-z
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

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

# 財務數據類
class FinancialData:
    def __init__(self):
        # 初始化餐飲業公司財務數據
        self.companies = {
            "85度C": {
                "code": "2723",
                "revenue_growth": {
                    "103": 8.5, "104": 10.2, "105": 7.8, "106": 5.5, "107": 3.2, 
                    "108": 2.1, "109": -5.8, "110": 4.2, "111": 8.5, "112": 6.2, "113": 7.5
                },
                "profit_margin": {
                    "103": 9.8, "104": 10.5, "105": 9.2, "106": 8.5, "107": 7.8, 
                    "108": 6.5, "109": 4.2, "110": 5.5, "111": 7.2, "112": 8.1, "113": 8.5
                },
                "roe": {
                    "103": 18.5, "104": 19.2, "105": 17.5, "106": 15.8, "107": 14.2, 
                    "108": 12.5, "109": 8.5, "110": 10.2, "111": 12.5, "112": 14.2, "113": 15.5
                },
                "debt_ratio": {
                    "103": 35.2, "104": 36.5, "105": 38.2, "106": 40.5, "107": 42.8, 
                    "108": 45.2, "109": 48.5, "110": 46.2, "111": 44.5, "112": 42.8, "113": 40.5
                },
                "eps": {
                    "103": 5.82, "104": 6.25, "105": 5.78, "106": 5.42, "107": 4.95, 
                    "108": 4.25, "109": 2.85, "110": 3.52, "111": 4.65, "112": 5.28, "113": 5.85
                }
            },
            "瓦城": {
                "code": "2729",
                "revenue_growth": {
                    "103": 15.8, "104": 18.5, "105": 20.2, "106": 22.5, "107": 18.5, 
                    "108": 12.5, "109": -8.5, "110": 5.2, "111": 15.8, "112": 18.5, "113": 20.2
                },
                "profit_margin": {
                    "103": 12.5, "104": 13.2, "105": 14.5, "106": 15.2, "107": 14.5, 
                    "108": 12.8, "109": 6.5, "110": 8.2, "111": 10.5, "112": 12.8, "113": 14.2
                },
                "roe": {
                    "103": 22.5, "104": 24.8, "105": 26.5, "106": 28.2, "107": 25.5, 
                    "108": 20.8, "109": 10.5, "110": 14.2, "111": 18.5, "112": 22.5, "113": 25.8
                },
                "debt_ratio": {
                    "103": 30.5, "104": 32.8, "105": 35.5, "106": 38.2, "107": 40.5, 
                    "108": 42.8, "109": 45.5, "110": 43.2, "111": 40.5, "112": 38.2, "113": 35.5
                },
                "eps": {
                    "103": 7.85, "104": 8.52, "105": 9.25, "106": 10.15, "107": 9.52, 
                    "108": 7.85, "109": 3.95, "110": 5.25, "111": 6.85, "112": 8.52, "113": 9.85
                }
            },
            "王品": {
                "code": "2727",
                "revenue_growth": {
                    "103": 12.5, "104": 10.8, "105": 8.5, "106": 5.2, "107": 3.5, 
                    "108": 2.8, "109": -12.5, "110": -5.2, "111": 8.5, "112": 12.5, "113": 15.8
                },
                "profit_margin": {
                    "103": 10.5, "104": 9.8, "105": 8.5, "106": 7.2, "107": 6.5, 
                    "108": 5.2, "109": 2.5, "110": 3.8, "111": 6.5, "112": 8.2, "113": 9.5
                },
                "roe": {
                    "103": 20.5, "104": 18.2, "105": 16.5, "106": 14.2, "107": 12.5, 
                    "108": 10.2, "109": 5.5, "110": 7.8, "111": 12.5, "112": 16.2, "113": 18.5
                },
                "debt_ratio": {
                    "103": 32.5, "104": 35.2, "105": 38.5, "106": 40.2, "107": 42.5, 
                    "108": 45.8, "109": 48.5, "110": 46.2, "111": 43.5, "112": 40.2, "113": 38.5
                },
                "eps": {
                    "103": 6.52, "104": 5.85, "105": 5.25, "106": 4.52, "107": 3.95, 
                    "108": 3.25, "109": 1.52, "110": 2.25, "111": 3.85, "112": 5.25, "113": 6.15
                }
            },
            "美食達人": {
                "code": "1259",
                "revenue_growth": {
                    "103": 22.5, "104": 25.8, "105": 28.5, "106": 30.2, "107": 25.5, 
                    "108": 20.8, "109": -2.5, "110": 8.5, "111": 15.2, "112": 18.5, "113": 22.5
                },
                "profit_margin": {
                    "103": 8.5, "104": 9.2, "105": 10.5, "106": 11.2, "107": 10.5, 
                    "108": 9.2, "109": 5.5, "110": 7.2, "111": 8.5, "112": 9.8, "113": 10.5
                },
                "roe": {
                    "103": 18.5, "104": 20.2, "105": 22.5, "106": 24.8, "107": 22.5, 
                    "108": 18.5, "109": 10.2, "110": 14.5, "111": 16.8, "112": 19.5, "113": 22.8
                },
                "debt_ratio": {
                    "103": 40.5, "104": 42.8, "105": 45.5, "106": 48.2, "107": 50.5, 
                    "108": 52.8, "109": 55.5, "110": 52.2, "111": 48.5, "112": 45.2, "113": 42.5
                },
                "eps": {
                    "103": 4.25, "104": 4.85, "105": 5.52, "106": 6.25, "107": 5.85, 
                    "108": 4.95, "109": 2.85, "110": 3.95, "111": 4.65, "112": 5.45, "113": 6.25
                }
            },
            "六角國際": {
                "code": "2732",
                "revenue_growth": {
                    "103": 18.5, "104": 20.2, "105": 22.5, "106": 24.8, "107": 20.5, 
                    "108": 15.2, "109": -5.5, "110": 3.8, "111": 10.5, "112": 15.2, "113": 18.5
                },
                "profit_margin": {
                    "103": 11.5, "104": 12.8, "105": 14.5, "106": 15.8, "107": 14.5, 
                    "108": 12.2, "109": 6.5, "110": 8.5, "111": 10.2, "112": 12.5, "113": 14.2
                },
                "roe": {
                    "103": 21.5, "104": 23.8, "105": 26.5, "106": 28.8, "107": 25.5, 
                    "108": 20.2, "109": 10.5, "110": 14.8, "111": 18.5, "112": 22.2, "113": 25.5
                },
                "debt_ratio": {
                    "103": 35.5, "104": 38.2, "105": 40.5, "106": 42.8, "107": 45.5, 
                    "108": 48.2, "109": 50.5, "110": 48.2, "111": 45.5, "112": 42.8, "113": 40.5
                },
                "eps": {
                    "103": 5.85, "104": 6.52, "105": 7.25, "106": 8.15, "107": 7.52, 
                    "108": 6.25, "109": 3.25, "110": 4.52, "111": 5.85, "112": 7.25, "113": 8.52
                }
            }
        }
        
        # 風險與亮點分析數據
        self.risk_highlight_data = {
            "85度C": {
                "111": {
                    "risks": [
                        "原物料成本上升壓縮利潤",
                        "國際連鎖咖啡品牌競爭加劇",
                        "疫情後消費習慣改變"
                    ],
                    "highlights": [
                        "數位轉型成效顯著，線上訂購成長",
                        "新產品線受到市場歡迎",
                        "營收成長率回升至8.5%"
                    ]
                },
                "112": {
                    "risks": [
                        "人力成本持續上升",
                        "租金成本增加",
                        "通膨壓力影響消費意願"
                    ],
                    "highlights": [
                        "會員經濟效益顯現",
                        "海外市場穩定成長",
                        "ESG策略獲得正面評價"
                    ]
                },
                "113": {
                    "risks": [
                        "市場競爭持續激烈",
                        "食品安全法規趨嚴",
                        "原物料價格波動"
                    ],
                    "highlights": [
                        "新店型展店策略成功",
                        "產品創新帶動客單價提升",
                        "數位行銷效益顯著"
                    ]
                }
            },
            "瓦城": {
                "111": {
                    "risks": [
                        "餐飲業人才短缺問題",
                        "多品牌管理複雜度增加",
                        "食材成本上漲"
                    ],
                    "highlights": [
                        "多品牌策略成功，市場覆蓋率高",
                        "營收成長率達15.8%",
                        "數位點餐系統提升營運效率"
                    ]
                },
                "112": {
                    "risks": [
                        "新品牌發展不確定性",
                        "國際擴張風險",
                        "消費者口味快速變化"
                    ],
                    "highlights": [
                        "高毛利新品牌表現亮眼",
                        "會員數持續成長",
                        "供應鏈優化降低成本"
                    ]
                },
                "113": {
                    "risks": [
                        "品牌老化風險",
                        "同業複製模式競爭",
                        "租金成本持續上升"
                    ],
                    "highlights": [
                        "品牌年輕化策略成功",
                        "海外市場貢獻增加",
                        "數位轉型成效顯著"
                    ]
                }
            },
            "王品": {
                "111": {
                    "risks": [
                        "高端餐飲市場競爭加劇",
                        "食材成本波動大",
                        "多品牌管理挑戰"
                    ],
                    "highlights": [
                        "疫後消費復甦明顯",
                        "新品牌發展順利",
                        "數位會員經濟成效顯著"
                    ]
                },
                "112": {
                    "risks": [
                        "中高價位餐飲受經濟環境影響大",
                        "人才流失風險",
                        "租金成本持續上升"
                    ],
                    "highlights": [
                        "品牌重塑策略成功",
                        "營運效率持續提升",
                        "多元化收入來源"
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
            },
            "美食達人": {
                "111": {
                    "risks": [
                        "快速擴張帶來的管理風險",
                        "品質一致性挑戰",
                        "中低價位市場競爭激烈"
                    ],
                    "highlights": [
                        "多元化餐飲品牌組合",
                        "數位點餐系統普及",
                        "外送業務成長顯著"
                    ]
                },
                "112": {
                    "risks": [
                        "原物料成本上升",
                        "人力成本增加",
                        "市場競爭加劇"
                    ],
                    "highlights": [
                        "新店型展店策略成功",
                        "會員經濟效益顯現",
                        "供應鏈整合降低成本"
                    ]
                },
                "113": {
                    "risks": [
                        "市場飽和風險",
                        "消費者偏好變化快速",
                        "食品安全法規趨嚴"
                    ],
                    "highlights": [
                        "產品創新帶動成長",
                        "數位行銷效益顯著",
                        "海外市場拓展順利"
                    ]
                }
            },
            "六角國際": {
                "111": {
                    "risks": [
                        "咖啡市場競爭激烈",
                        "原物料成本上升",
                        "租金成本增加"
                    ],
                    "highlights": [
                        "多品牌策略成功",
                        "數位轉型成效顯著",
                        "會員經濟效益顯現"
                    ]
                },
                "112": {
                    "risks": [
                        "國際擴張風險",
                        "品牌間同質化風險",
                        "人才短缺問題"
                    ],
                    "highlights": [
                        "ESG策略獲得正面評價",
                        "產品創新帶動客單價提升",
                        "供應鏈優化降低成本"
                    ]
                },
                "113": {
                    "risks": [
                        "市場飽和風險",
                        "消費者偏好變化快速",
                        "食品安全法規趨嚴"
                    ],
                    "highlights": [
                        "海外市場貢獻增加",
                        "數位會員經濟成效顯著",
                        "新店型展店策略成功"
                    ]
                }
            }
        }
        
        # 指標中文名稱對照
        self.metric_names = {
            "revenue_growth": "營收成長率 (%)",
            "profit_margin": "淨利率 (%)",
            "roe": "股東權益報酬率 (%)",
            "debt_ratio": "負債比率 (%)",
            "eps": "每股盈餘 (元)"
        }
        
        # 年度列表
        self.years = ["103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113"]
    
    def get_company_names(self):
        """獲取所有公司名稱"""
        return list(self.companies.keys())
    
    def get_company_code(self, company_name):
        """獲取公司代碼"""
        return self.companies[company_name]["code"]
    
    def get_metric_names(self):
        """獲取所有指標名稱"""
        return self.metric_names
    
    def get_years(self):
        """獲取所有年度"""
        return self.years
    
    def get_data_for_years(self, company_name, metric, years_range):
        """獲取特定年份範圍的數據"""
        if years_range == 5:
            selected_years = self.years[-5:]
        else:  # 10年
            selected_years = self.years[-10:]
        
        return {year: self.companies[company_name][metric][year] for year in selected_years}
    
    def get_risk_highlight(self, company_name, year):
        """獲取風險與亮點分析"""
        if company_name in self.risk_highlight_data and year in self.risk_highlight_data[company_name]:
            return self.risk_highlight_data[company_name][year]
        else:
            return {"risks": ["無該年度風險資料"], "highlights": ["無該年度亮點資料"]}


# 圖表生成類
class ChartGenerator:
    def __init__(self, financial_data):
        self.financial_data = financial_data
    
    def generate_line_chart(self, selected_companies, metric, years_range):
        """生成折線圖"""
        if years_range == 5:
            selected_years = self.financial_data.get_years()[-5:]
        else:  # 10年
            selected_years = self.financial_data.get_years()[-10:]
        
        fig = go.Figure()
        
        for company in selected_companies:
            data = self.financial_data.get_data_for_years(company, metric, years_range)
            values = [data[year] for year in selected_years]
            
            fig.add_trace(go.Scatter(
                x=selected_years,
                y=values,
                mode='lines+markers',
                name=f"{company} ({self.financial_data.get_company_code(company)})",
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title=f"{self.financial_data.get_metric_names()[metric]} 趨勢圖",
            xaxis_title="年度",
            yaxis_title=self.financial_data.get_metric_names()[metric],
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
    
    def generate_comparison_table(self, company, year):
        """生成年度比較表格數據"""
        prev_year = str(int(year) - 1)
        metrics = ["revenue_growth", "profit_margin", "roe", "debt_ratio", "eps"]
        
        comparison_data = []
        
        for metric in metrics:
            current_value = self.financial_data.companies[company][metric][year]
            prev_value = self.financial_data.companies[company][metric][prev_year]
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
                "metric": self.financial_data.metric_names[metric],
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
        self.financial_data = FinancialData()
        self.chart_generator = ChartGenerator(self.financial_data)
    
    def run(self):
        """運行應用程序"""
        st.markdown("<h1 style='text-align: center; color: #581845;'>餐飲業財務分析儀表板</h1>", unsafe_allow_html=True)
        
        # 側邊欄 - 公司選擇
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
            list(self.financial_data.get_metric_names().keys()),
            format_func=lambda x: self.financial_data.get_metric_names()[x]
        )
        
        # 主要內容區域
        if not selected_companies:
            st.warning("請至少選擇一家公司進行分析")
            return
        
        # 生成圖表
        st.markdown("### 財務指標趨勢圖")
        fig = self.chart_generator.generate_line_chart(selected_companies, selected_metric, years_range)
        st.plotly_chart(fig, use_container_width=True)
        
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
            if years_range == 5:
                available_years = self.financial_data.get_years()[-5:]
            else:
                available_years = self.financial_data.get_years()[-10:]
            
            selected_year = st.selectbox(
                "選擇年度",
                available_years,
                index=len(available_years)-1,
                format_func=lambda x: f"{x}年",
                key="year_detail"
            )
        
        # 生成比較表格
        comparison_data, prev_year = self.chart_generator.generate_comparison_table(company_for_detail, selected_year)
        
        st.markdown(f"#### {company_for_detail} ({self.financial_data.get_company_code(company_for_detail)}) {selected_year}年 vs {prev_year}年 財務比較")
        
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
        
        risk_highlight = self.financial_data.get_risk_highlight(company_for_detail, selected_year)
        
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
        
        company_info = {
            "85度C": {
                "full_name": "美食-KY",
                "industry": "連鎖咖啡烘焙",
                "founded": "2004年",
                "stores": "全球超過1,000家門市",
                "description": "以現烤麵包、現煮咖啡聞名的連鎖咖啡烘焙店，在台灣、中國、美國等地均有據點。"
            },
            "瓦城": {
                "full_name": "瓦城泰統集團",
                "industry": "連鎖餐飲",
                "founded": "1990年",
                "stores": "超過100家門市",
                "description": "以泰式料理起家，旗下擁有瓦城、非常泰、1010湘、十食湘、時時香、YABI等多個品牌。"
            },
            "王品": {
                "full_name": "王品集團",
                "industry": "連鎖餐飲",
                "founded": "1993年",
                "stores": "超過400家門市",
                "description": "台灣知名連鎖餐飲集團，旗下擁有王品牛排、陶板屋、西堤、夏慕尼等多個品牌。"
            },
            "美食達人": {
                "full_name": "美食達人股份有限公司",
                "industry": "連鎖餐飲",
                "founded": "1996年",
                "stores": "超過200家門市",
                "description": "以平價美食聞名，旗下擁有多個中式、日式、西式餐飲品牌，主打年輕消費族群。"
            },
            "六角國際": {
                "full_name": "六角國際事業股份有限公司",
                "industry": "連鎖咖啡餐飲",
                "founded": "1998年",
                "stores": "超過300家門市",
                "description": "以咖啡起家，旗下擁有cama café、路易莎咖啡、棉花田等多個品牌，近年積極拓展海外市場。"
            }
        }
        
        info = company_info[company_for_detail]
        
        st.markdown(f"""
        <div class="highlight">
            <h5>{company_for_detail} ({self.financial_data.get_company_code(company_for_detail)}) - {info['full_name']}</h5>
            <p><strong>產業類別:</strong> {info['industry']}</p>
            <p><strong>成立時間:</strong> {info['founded']}</p>
            <p><strong>門市規模:</strong> {info['stores']}</p>
            <p><strong>公司簡介:</strong> {info['description']}</p>
        </div>
        """, unsafe_allow_html=True)


# 執行應用程序
if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.run()