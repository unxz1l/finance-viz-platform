from modules.data_loader import fetch_statement

def test_fetch_is():
    df = fetch_statement(2023, 2, "is")
    assert "2330" in df.index        # 台積電Q3
    assert df.shape[0] > 50