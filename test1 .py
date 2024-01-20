# import pandas as pd

# # 創建一個範例 DataFrame
# data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
# df = pd.DataFrame(data)

# # 顯示原始 DataFrame
# print("原始 DataFrame:")
# print(df)

# # 移除索引
# df_reset = df.reset_index(drop=True)

# # 顯示移除索引後的 DataFrame
# print("\n移除索引後的 DataFrame:")
# print(df_reset)
# from db_select import *
# import talib

# def calculate_technical_indicators(data):
    
#     # RSI (相對強弱指標)
#     data['RSI'] = talib.RSI(data['Adj Close'], timeperiod=14)

#     # MA20 (移動平均線)
#     data['MA20'] = talib.SMA(data['Adj Close'], timeperiod=20)

#     # MA50 (移動平均線)
#     data['MA50'] = talib.SMA(data['Adj Close'], timeperiod=50)

#     # MACD (移動平均收斂與分歧)
#     data['MACD'], data['Signal_Line'], _ = talib.MACD(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)

#     # KD (隨機指標)
#     data['K'], data['D'] = talib.STOCH(data['High'], data['Low'], data['Adj Close'], fastk_period=9, slowk_period=3, slowd_period=3)

#     return data

# result = select_data()
# # filtered_df = result[result['stock_n'] == "2330.TW"]
# # print(result.columns)
# stock_data = result.loc[result['stock_n'] == "2330.TW"]
# print("----------------")
# print(stock_data.columns)
# print("----------------")
# data_1 = calculate_technical_indicators(stock_data)
# # stock_data['RSI'] = talib.RSI(stock_data['Adj Close'], timeperiod=14)
# print(data_1)
# print("-----filtered_df-----")
# print(filtered_df)
# print("-----stock_data-----")
# print(stock_data)
# print("-----stock_data['RSI']-----")
# print(stock_data['RSI'])

# import datetime
# import pandas as pd
# # current_date = datetime.date.today()
# # previous_date = current_date - datetime.timedelta(days=1)
# # print(current_date)
# # print(previous_date)
# result = pd.read_csv("result.csv")
# # print(type(result))
# # for row in result:
# #     print(row)

# # 逐行印出 DataFrame 中的每一行
# import pandas as pd


# 逐行印出 DataFrame 中的每一行
# for index, row in result.iterrows():
#     print(f"股票代號: {row['SYMBOL']}")
#     print(f"Date: {row['Date']}")
#     print(f"關注: {row['Action']}")
#     print("-------------------")
# import psycopg2
# from psycopg2 import sql
# import datetime

# # 連接到 PostgreSQL 資料庫
# conn = psycopg2.connect(
#     host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
#     user="stock_zs94_user",
#     password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
#     database="stock_zs94"   
# )

# cursor = conn.cursor()

# # 欲查詢的目標日期
# target_date = datetime.date.today()

# # 撈取最接近目標日期的一筆資料
# query = sql.SQL("SELECT * FROM stockdb ORDER BY ABS(date - %s) LIMIT 1;")
# cursor.execute(query, (target_date,))
# result = cursor.fetchone()
# print(result[1])
# # 處理查詢結果，result 包含最接近日期的資料

# # 關閉資料庫連線
# cursor.close()
# conn.close()


# from date import latestdate
# latest_date = latestdate()
# print(str(latest_date))
# print(type('2024-01-15'))


# import pandas as pd
# result = pd.read_csv("result.csv")
# num_rows, num_columns = result.shape
# print(result.iloc[0,:].values)
# table_name = "signals"
# for row in range(1,num_rows):
#     stock_values = tuple(result.iloc[row,:].values)
#     sql_query = f"insert into {table_name} values {stock_values}"
#     print(sql_query)

# import psycopg2
# from psycopg2 import sql
# import pandas as pd
# # 建立資料庫連線
# def signal_data():
#     conn = psycopg2.connect(
#         host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
#         user="stock_zs94_user",
#         password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
#         database="stock_zs94"   
#     )

#     # 建立一個 cursor 物件
#     cursor = conn.cursor()

#     # 動態組合 SQL 查詢，使用 TO_CHAR 函數將日期格式化
#     table_name = "signals"
#     date_format = "YYYY-MM-DD"  # 你想要的日期格式
#     sql_query = f"SELECT symbol, date, action FROM {table_name}"
#     cursor.execute(sql_query)
#     # 獲取所有結果
#     signal_data = cursor.fetchall()
#     signal_data = pd.DataFrame(signal_data)
#     signal_data.columns = ['symbol', 'date', 'action']
#     cursor.execute
#     # 提交變更
#     conn.commit()

#     # 關閉 cursor 和連線
#     cursor.close()
#     conn.close()

#     return signal_data

# result = signal_data()
# if result.empty:
#         print("今日無適當進出場時機，繼續持有等待時機!")
# else:    
#     for index, row in result.iterrows():
#         print(f"股票代號: {row['symbol']}")
#         print(f"Date: {row['date']}")
#         print(f"關注: {row['action']}")
#         print("-------------------")