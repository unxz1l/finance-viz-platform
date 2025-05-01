import logging
from finance_analyzer.data.loader import fetch_statement
import pandas as pd

# 設定日誌
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def test_fetch_restaurant_companies():
    # 測試的餐飲公司列表
    restaurant_companies = [
        "2727",  # 王品餐飲
        "2729",  # 瓦城泰統
        "2753",  # 八方雲集
        "1259",  # 安心食品服務
        "1268",  # 漢來美食
        "7708",  # 全家國際餐飲
        "7705",  # 三商餐飲
        "2752",  # 豆府
        "4419"   # 皇家可口
    ]
    
    try:
        print("\n嘗試從 TWSE 抓取損益表資料...")
        is_df_twse = fetch_statement("is", market="twse")
        if is_df_twse is not None:
            print(f"TWSE 資料形狀: {is_df_twse.shape}")
            print("TWSE 資料欄位:")
            print(is_df_twse.columns.tolist())
            print("TWSE 資料前幾筆:")
            print(is_df_twse.head())
        
        print("\n嘗試從 TPEX 抓取損益表資料...")
        is_df_tpex = fetch_statement("is", market="tpex")
        if is_df_tpex is not None:
            print(f"TPEX 資料形狀: {is_df_tpex.shape}")
            print("TPEX 資料欄位:")
            print(is_df_tpex.columns.tolist())
            print("TPEX 資料前幾筆:")
            print(is_df_tpex.head())
        
        # 合併兩個市場的數據
        is_df = pd.concat([is_df_twse, is_df_tpex]) if is_df_twse is not None and is_df_tpex is not None else None
        
        if is_df is not None and not is_df.empty:
            print(f"\n合併後資料形狀: {is_df.shape}")
            print("合併後資料欄位:")
            print(is_df.columns.tolist())
            
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
                print("\n找到的公司資料：")
                for company in found_companies:
                    print(f"\n{company} 的資料:")
                    print(is_df.loc[company])
                assert True
            else:
                print("\n沒有找到任何餐飲公司的資料")
                assert False, "沒有找到任何餐飲公司的資料"
        else:
            assert False, "無法抓取損益表資料"
            
    except Exception as e:
        print(f"抓取資料時發生錯誤: {str(e)}")
        assert False, f"抓取資料時發生錯誤: {str(e)}"

if __name__ == "__main__":
    test_fetch_restaurant_companies()