# modules/data_loader.py
from pathlib import Path
import time, requests, pandas as pd

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

URLS = {
    "is": "https://mops.twse.com.tw/mops/web/ajax_t163sb04",   # 損益表
    "bs": "https://mops.twse.com.tw/mops/web/ajax_t163sb05",   # 資產負債表
}

def _roc(year):        # 轉民國年
    return year - 1911

def _payload(year, season, market="sii"):
    return {
        "encodeURIComponent": 1, "step": 1, "firstin": 1, "off": 1,
        "TYPEK": market,
        "year":  str(_roc(year)),
        "season": f"{season:02d}",
    }

def fetch_statement(year:int, season:int, table:str, retry:int=3):
    assert table in URLS, "table 必須是 'is' 或 'bs'"
    csv_path = RAW_DIR / f"{table}_{year}_{season}.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path, index_col=0)

    for i in range(retry):
        r = requests.post(URLS[table], _payload(year, season), timeout=30)
        if "html" not in r.headers.get("Content-Type",""):
            time.sleep(2); continue                      # 伺服器偶爾回空白
        r.encoding = "utf8"
        dfs = pd.read_html(r.text, header=None)
        if len(dfs) < 2:                                # 第 0 張常是說明文字
            time.sleep(2); continue
        df = (pd.concat(dfs[1:], ignore_index=True)     # 合併多張
                .iloc[:, :-1]                           # 去掉「合計」欄
                .set_index(dfs[1].columns[0])
                .apply(pd.to_numeric, errors="coerce"))
        df.to_csv(csv_path)                             # 快取
        return df
    raise RuntimeError(f"抓取失敗：{table} {year}Q{season}")