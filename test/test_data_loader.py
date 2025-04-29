import logging
from finance_analyzer.data.loader import fetch_statement

# 設定日誌
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def test_fetch_restaurant_companies():
    # 測試的餐飲公司列表
    restaurant_companies = [
        "2727",  # 王品餐飲
        "2729",  # 瓦城泰統
        "2753",  # 八方雲集
        "1260",  # 乾杯
        "1259",  # 安心食品服務
        "1268",  # 漢來美食
        "7708",  # 全家國際餐飲
        "1277",  # 三商餐飲
        "2752",  # 豆府
        "4419"   # 皇家可口
    ]
    
    try:
        print("\n嘗試抓取損益表資料...")
        is_df = fetch_statement("is")
        
        if is_df is not None and not is_df.empty:
            print(f"成功抓取損益表資料！")
            print(f"資料形狀: {is_df.shape}")
            
            # 檢查每個公司是否都在資料中
            found_companies = []
            missing_companies = []
            for company in restaurant_companies:
                if company in is_df.index:
                    found_companies.append(company)
                else:
                    missing_companies.append(company)
            
            print(f"\n找到的公司: {found_companies}")
            print(f"未找到的公司: {missing_companies}")
            
            if found_companies:
                print("\n部分公司資料範例：")
                print(is_df.loc[found_companies].head())
                assert True
            else:
                print("\n沒有找到任何餐飲公司的資料")
                assert False, "沒有找到任何餐飲公司的資料"
        else:
            assert False, "無法抓取損益表資料"
            
    except Exception as e:
        print(f"抓取資料時發生錯誤: {str(e)}")
        assert False, f"抓取資料時發生錯誤: {str(e)}"