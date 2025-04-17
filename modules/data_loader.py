from pathlib import Path
import time, requests, pandas as pd
from io import StringIO

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

URLS = {
    "is": "https://mops.twse.com.tw/nas/t21/{TYPEK}/t163sb04_{rocYear}_{season}_0.csv",   # 損益表
    "bs": "https://mops.twse.com.tw/nas/t21/{TYPEK}/t163sb05_{rocYear}_{season}_0.csv",   # 資產負債表
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

import random, textwrap
HEADERS = {
"User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9",
    "Referer": "https://mops.twse.com.tw/mops/web/t163sb04",  # or 05
}

# --- keep one persistent session to reuse cookies / keep‑alive ---
SESSION = requests.Session()
SESSION.headers.update(HEADERS | {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
})

def fetch_statement(year: int, season: int, table: str, retry: int = 3, sleep: float = 2.0):
    """
    Download a quarterly statement table (income‑statement or balance‑sheet).

    Parameters
    ----------
    year   : Gregorian year, e.g. 2023
    season : 1–4
    table  : "is" for income‑statement, "bs" for balance‑sheet
    """
    assert table in URLS, "table 必須是 'is' 或 'bs'"

    csv_path = RAW_DIR / f"{table}_{year}_{season}.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path, index_col=0)

    referer_page = f"https://mops.twse.com.tw/mops/web/t163sb{'04' if table == 'is' else '05'}"
    ajax_url = URLS[table]

    for i in range(retry):
        # warm‑up: fetch the normal HTML page once to obtain cookies
        if i == 0:
            try:
                SESSION.get(referer_page, timeout=15)
            except requests.RequestException:
                pass

        hdrs = {
            **SESSION.headers,
            "Referer": referer_page,
            "Origin": "https://mops.twse.com.tw",
            "X-Requested-With": "XMLHttpRequest",
        }

        try:
            resp = SESSION.post(ajax_url, _payload(year, season), headers=hdrs, timeout=30)
        except requests.RequestException:
            time.sleep(sleep * (i + 1))
            continue

        resp.encoding = "utf8"
        text = resp.text

        if "THE PAGE CANNOT BE ACCESSED" in text:
            time.sleep(sleep * (i + 1))
            continue  # very likely blocked; back‑off and retry

        # try parsers in order
        for parser in ("lxml", "html5lib"):
            try:
                dfs = pd.read_html(StringIO(text), header=None, flavor=parser)
                if len(dfs) >= 2:
                    df = (
                        pd.concat(dfs[1:], ignore_index=True)
                        .iloc[:, :-1]
                        .set_index(dfs[1].columns[0])
                        .apply(pd.to_numeric, errors="coerce")
                    )
                    df.to_csv(csv_path)
                    return df
            except ValueError:
                # parser could not find tables
                continue

        # if we reach here, either table not yet published or blocked; wait & retry
        time.sleep(sleep * (i + 1))

    raise RuntimeError(f"抓取失敗：{table} {year}Q{season}")

if __name__ == "__main__":
    import pprint
    html = requests.post(
        URLS["is"],
        _payload(2023, 3),        # 你要的季度
        headers={
            **HEADERS,
            "Referer": "https://mops.twse.com.tw/mops/web/t163sb04",
        },
        timeout=30,
    ).text
    print("=== 前 500 文字 ===")
    print(html[:500])