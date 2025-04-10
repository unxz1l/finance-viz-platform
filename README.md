# 📊 Financial Indicator Visualization Platform｜財務指標視覺化平台

A Streamlit-based platform that helps non-professional investors visualize and understand key financial indicators of public companies.  
本平台使用 Streamlit 製作，協助非專業投資人理解公開公司之財務指標與投資風險。

> Developed as a course project for *Introduction to Programming (Code: 11320QF100300)*  
> Department of Quantitative Finance, National Tsing Hua University  
> Instructor: Prof. Cheng-Chi Chen (陳政琦)

> 本專案為清華大學計量財務金融學系《計算機程式設計》（課號：11320QF100300）課程之專題作業，指導教師為陳政琦教授。

---

## 🌟 Features | 特色功能

- 🔍 Select companies (e.g., Wowprime, Kanpai, Bafang Yunji) and fiscal year  
  → 下拉選單選擇公司與年份
- 📈 Visualize trends of key financial indicators over the past 5–10 years  
  → 顯示 5～10 年財務指標趨勢圖（如 ROE、營收成長率）
- 🧠 Auto-compare selected year with previous year and generate insights  
  → 自動與前一年比較，產出亮點 / 風險語句

---

## 🛠 Technologies Used | 技術架構

- Python 3.9+
- Streamlit
- Pandas / Numpy
- Matplotlib or Plotly
- Data Source: Taiwan MOPS 財報資料（公開資訊觀測站）

---

## 📁 Folder Structure | 資料夾架構

```text
finance-viz-platform/
│
├── data/                  # 財報原始資料（CSV 檔）
├── modules/               # 核心功能模組
│   ├── data_loader.py     # 資料讀取與清洗
│   ├── indicators.py      # 財務指標計算
│   ├── visualizer.py      # 圖表視覺化
│   └── insights.py        # 自動判讀語句生成
├── pages/                 # Streamlit 多頁面設計
│   ├── 1_select_company.py
│   ├── 2_trend_view.py
│   └── 3_compare_years.py
├── app.py                 # 主入口
└── requirements.txt       # 相依套件

```

## 🚀 Installation & Usage | 安裝與執行

git clone https://github.com/unxz1l/finance-viz-platform.git
cd finance-viz-platform
pip install -r requirements.txt
streamlit run app.py

---

## 🔮 Future Plans | 未來規劃
	•	Extend data format to support SQLite / API
擴充資料儲存格式，支援 SQLite 或 API
	•	Add more financial indicators (EPS, gross margin, etc.)
增加更多財務指標（如 EPS、毛利率）
	•	Refine interpretation logic using NLP templates
精化判讀語句邏輯，考慮加入 NLP 模型或模板

---

## 🙌 Credits | 致謝
	•	Inspired by StatementCloud and MOPS
	•	National Tsing Hua University, Department of Quantitative Finance
	•	Course: Introduction to Programming（計算機程式設計）｜Code: 11320QF100300
Instructor: Prof. Cheng-Chi Chen（陳政琦教授）
