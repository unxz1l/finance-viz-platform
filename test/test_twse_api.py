import requests
import json
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def test_twse_api():
    # TWSE API 端點
    base_url = "https://openapi.twse.com.tw/v1"
    endpoint = "/exchangeReport/BWIBBU_d"
    
    # 測試的上市公司
    companies = [
        "2727",  # 王品
        "2729",  # 瓦城
        "2753",  # 八方雲集
        "7705",  # 三商餐飲
        "2723",  # 美食-KY
        "2732"   # 六角國際
    ]
    
    # 設定請求標頭
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        # 發送請求
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        logging.info(f"API 回應狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            # 解析 JSON 回應
            data = response.json()
            logging.info(f"API 返回資料筆數: {len(data)}")
            
            # 檢查每個公司的資料
            for company in companies:
                company_data = [item for item in data if item.get("Code") == company]
                if company_data:
                    logging.info(f"找到公司 {company} 的資料:")
                    logging.info(json.dumps(company_data[0], ensure_ascii=False, indent=2))
                else:
                    logging.warning(f"未找到公司 {company} 的資料")
            
            # 檢查資料格式
            if data:
                logging.info("\n資料欄位範例:")
                logging.info(json.dumps(data[0], ensure_ascii=False, indent=2))
        else:
            logging.error(f"API 請求失敗: {response.text}")
            
    except Exception as e:
        logging.error(f"測試過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    test_twse_api() 