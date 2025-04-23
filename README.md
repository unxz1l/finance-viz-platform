# 📊 Financial Indicator Visualization Platform｜財務指標視覺化平台

A **Streamlit**‑based application that helps *non‑professional investors* visualize and understand the key financial indicators of Taiwanese public companies.

本平台使用 **Streamlit** 製作，協助非專業投資人快速理解台灣上市櫃公司之財務指標與投資風險。

> Developed as a course project for *Introduction to Programming* (Course Code 11320QF100300)  
> Department of Quantitative Finance, National Tsing Hua University  
> Instructor 指導教師：Prof. Cheng‑Chi Chen 陳政琦

---

## 🌟 Features｜特色功能

|  | Feature | 說明 |
|---|---|---|
| 🔍 | **Company & Fiscal Year Selection** | 下拉選單快速選擇公司（如 2727 Wowprime、1262 Kanpai）與財報年度／季度 |
| 📈 | **Multi‑year Trend Charts** | 顯示近 5 – 10 年核心財務指標折線圖（ROE、營收 YoY、營業淨利 YoY…） |
| 🧠 | **Auto Insight Generation** | 一鍵與前期比較，產出亮點／風險語句 |

---

## 🛠 Tech Stack｜技術架構

- **Python 3.9+**
- **Streamlit** (for UI)
- **Pandas / NumPy** (data wrangling)
- **Matplotlib / Seaborn** (visualization)
- **Requests** (data fetching)
- **Data Source 資料來源**：Taiwan MOPS (公開資訊觀測站) financial statements

---

## 📁 Folder Structure｜資料夾架構

```
finance_analyzer/
├── README.md                  # 專案文檔
├── requirements.txt           # 依賴管理
├── setup.py                   # 包安裝配置
├── .gitignore                 # Git忽略文件
├── finance_analyzer/          # 主代碼包
│   ├── __init__.py
│   ├── config.py              # 配置管理
│   ├── data/                  # 數據處理相關
│   │   ├── __init__.py
│   │   ├── loader.py          # 負責從台灣證券交易所獲取財務數據
│   │   └── processor.py       # 數據預處理和轉換
│   ├── analysis/              # 分析相關
│   │   ├── __init__.py
│   │   ├── indicators.py      # 計算財務指標如ROE等
│   │   └── insights.py        # 生成財務見解和解讀
│   ├── visualization/         # 視覺化相關
│   │   ├── __init__.py
│   │   └── plotter.py         # 數據視覺化圖表生成
│   └── utils/                 # 通用工具
│       ├── __init__.py
│       └── helpers.py         # 輔助函數
├── tests/                     # 測試目錄
│   ├── __init__.py
│   ├── test_loader.py         # 數據加載測試
│   └── test_indicators.py     # 指標計算測試
└── app/                       # 應用界面
    ├── __init__.py
    ├── app.py                 # 主Streamlit應用
    └── pages/                 # 多頁面應用
        ├── __init__.py
        ├── 1_select_company.py  # 公司和年度選擇頁面
        ├── 2_trend_view.py      # 財務指標趨勢展示頁面
        └── 3_compare_years.py   # 年度比較與解讀頁面
```

---

## 🔑 核心財務指標

本平台專注於三個關鍵財務指標，協助投資人快速判斷企業財務健康狀況：

1. **股東權益報酬率 (ROE)**
   - 衡量公司利用股東資金創造利潤的效率
   - 一般而言，高ROE代表公司有效利用股東投資產生收益

2. **營收成長率 (Revenue Growth Rate)**
   - 衡量公司業務擴張速度
   - 持續正向的成長率表示公司業務穩定發展

3. **營業淨利成長率 (Operating Margin Growth Rate)**
   - 衡量公司提高營運效率的能力
   - 正向成長意味著公司能更有效率地將營收轉化為利潤

---

## 🚀 Getting Started｜快速開始

Follow the steps below **in your local terminal** (not inside any *.py* file):

```bash
# 1. Clone the repo
$ git clone https://github.com/yourusername/finance-viz-platform.git
$ cd finance-viz-platform

# 2. (Optional) Create & activate a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Launch the app
$ streamlit run app/app.py
```

> **Tip 💡** If you prefer a one‑liner, create a `Makefile` with an `init` target that wraps steps 2‑3.

---

## 📦 Dependencies

主要依賴套件已列在 `requirements.txt` 中，包括：

```
pandas
numpy
matplotlib
seaborn
streamlit
requests
lxml
html5lib
```

---

## 🗺 Roadmap｜未來規劃

- **Data Source Abstraction** → 支援 SQLite / REST API
- **More Indicators** → EPS, Gross Margin, Cash Flow ratios…
- **Insight Engine Upgrade** → NLP templates / LLM for richer explanations
- **Async Fetcher** → aiohttp for faster multi‑year scraping
- **CI / CD** → GitHub Actions + Streamlit Community Cloud auto deploy

---

## 💻 Development Guidelines｜開發指南

### 添加新指標

1. 在 `analysis/indicators.py` 的 `FinancialIndicators` 類中添加新的計算方法
2. 在 `DEFAULT_INDICATORS` 常量中添加新指標
3. 在 `analysis/insights.py` 中添加相應的見解生成邏輯

### 添加新的視覺化圖表

1. 在 `visualization/plotter.py` 的 `FinancialPlotter` 類中添加新的繪圖方法
2. 在相應的頁面模組中使用新的視覺化方法

---

## 🙌 Credits｜致謝

- Inspired by **StatementCloud** and Taiwan **MOPS (公開資訊觀測站)**
- National Tsing Hua University • Department of Quantitative Finance
- Course：*Introduction to Programming*（計算機程式設計） Code 11320QF100300
- Instructor：Prof. Cheng‑Chi Chen 陳政琦教授
