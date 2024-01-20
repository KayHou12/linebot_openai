import psycopg2
from psycopg2 import sql
import pandas as pd
# 建立資料庫連線
def select_data():
    conn = psycopg2.connect(
        host="dpg-cmj44gocmk4c739n03bg-a.oregon-postgres.render.com",
        user="db_4qcx_user db_4qcx",
        password="diKiHADHIiXgWkRa8TrxA57mQt07Jx23",
        database="db_4qcx"
    )

    # 建立一個 cursor 物件
    cursor = conn.cursor()

    # 動態組合 SQL 查詢，使用 TO_CHAR 函數將日期格式化
    table_name = "stockdb"
    date_format = "YYYY-MM-DD"  # 你想要的日期格式
    sql_query = f"SELECT stock_n, TO_CHAR(date, '{date_format}') AS formatted_date, open, high, low, close, \"Adj Close\", volume FROM {table_name} limit 10"
    cursor.execute(sql_query)
    # 獲取所有結果
    stock_data = cursor.fetchall()
    stock_data = pd.DataFrame(stock_data)
    stock_data.columns = ['stock_n', 'date', 'open', 'high', ' low', 'close','Adj Close', 'volume']
    stock_data.reset_index(drop=True)
    cursor.execute
    # 提交變更
    conn.commit()

    # 關閉 cursor 和連線
    cursor.close()
    conn.close()

    return stock_data

def select_stock_n():
    conn = psycopg2.connect(
        host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
        user="stock_zs94_user",
        password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
        database="stock_zs94"   
    )

    # 建立一個 cursor 物件
    cursor = conn.cursor()

    # 動態組合 SQL 查詢唯一值
    table_name = "stockdb"
    sql_query = f"SELECT DISTINCT stock_n FROM {table_name}"
    cursor.execute(sql_query)
    # 獲取所有結果
    unique_stock_name = cursor.fetchall()

    cursor.execute
    # 提交變更
    conn.commit()

    # 關閉 cursor 和連線
    cursor.close()
    conn.close()
    unique_stock_name = [item[0] for item in unique_stock_name]
    return unique_stock_name

import yfinance as yf
def get_stock_data(symbol, start_date):
    stock_data = yf.download(symbol, start=start_date)
    return stock_data
result = get_stock_data('2330.TW','2024-01-08')
print(result)

result1 = select_data()
print(result1)