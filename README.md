# 📊 Financial Indicator Visualization Platform｜財務指標視覺化平台

A **Streamlit**‑based application that helps *non‑professional investors* visualize and understand the key financial indicators of Taiwanese public companies.

本平台使用 **Streamlit** 製作，協助非專業投資人快速理解台灣上市櫃公司之財務指標與投資風險。

> Developed as a course project for *Introduction to Programming* (Course Code 11320QF100300)  
> Department of Quantitative Finance, National Tsing Hua University  
> Instructor 指導教師：Prof. Cheng‑Chi Chen 陳政琦

---

## 🌟 Features｜特色功能

|  | Feature | 說明 |
|---|---|---|
| 🔍 | **Company & Fiscal Year Selection** | 下拉選單快速選擇公司（如 2727 Wowprime、1262 Kanpai）與財報年度／季度 |
| 📈 | **Multi‑year Trend Charts** | 顯示近 5 – 10 年核心財務指標折線圖（ROE、營收 YoY、營業淨利 YoY…） |
| 🧠 | **Auto Insight Generation** | 一鍵與前期比較，產出亮點／風險語句 |

---

## 🛠 Tech Stack｜技術架構

- **Python 3.9 +**
- **Streamlit** (for UI)
- **Pandas / NumPy** (data wrangling)
- **Matplotlib or Plotly** (visualization)
- **Data Source 資料來源**：Taiwan MOPS (公開資訊觀測站) financial statements

---

## 📁 Folder Structure｜資料夾架構

```text
finance-viz-platform/
│
├── data/                  # 財報原始資料（CSV）
├── modules/               # 核心功能模組
│   ├── data_loader.py     # 資料抓取 / 清洗
│   ├── indicators.py      # 財務指標計算
│   ├── visualizer.py      # 圖表視覺化
│   └── insights.py        # 自動判讀語句生成
├── pages/                 # Streamlit 多頁面
│   ├── 1_select_company.py
│   ├── 2_trend_view.py
│   └── 3_compare_years.py
├── app.py                 # Streamlit 主入口
├── requirements.txt       # 相依套件
└── .gitignore             # Git 忽略項
```

---

## 🚀 Getting Started｜快速開始

Follow the steps below **in your local terminal** (not inside any *.py* file):

```bash
# 1. Clone the repo
$ git clone https://github.com/unxz1l/finance-viz-platform.git
$ cd finance-viz-platform

# 2. (Optional) Create & activate a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Launch the app
$ streamlit run app.py
```

> **Tip 💡** If you prefer a one‑liner, create a `Makefile` with an `init` target that wraps steps 2‑3.

---

## 📦 Requirements.txt

```text
pandas
requests
tqdm
streamlit
matplotlib   # or plotly
```

> 為保持彈性，目前未鎖版本。待專案穩定後再以 `pip‑compile` 產生 lock file。

---

## 🗺 Roadmap｜未來規劃

- **Data Source Abstraction** → 支援 SQLite / REST API
- **More Indicators** → EPS, Gross Margin, Cash Flow ratios…
- **Insight Engine Upgrade** → NLP templates / LLM for richer explanations
- **Async Fetcher** → aiohttp for faster multi‑year scraping
- **CI / CD** → GitHub Actions + Streamlit Community Cloud auto deploy

---

## 🙌 Credits｜致謝

- Inspired by **StatementCloud** and Taiwan **MOPS (公開資訊觀測站)**
- National Tsing Hua University • Department of Quantitative Finance
- Course：*Introduction to Programming*（計算機程式設計） Code 11320QF100300
- Instructor：Prof. Cheng‑Chi Chen 陳政琦教授

