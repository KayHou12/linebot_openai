import psycopg2
from psycopg2 import sql

# 建立資料庫連線
conn = psycopg2.connect(
    host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
    user="stock_zs94_user",
    password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
    database="stock_zs94"   
)

# 建立一個 cursor 物件
cursor = conn.cursor()

# 動態組合 SQL 查詢，使用 TO_CHAR 函數將日期格式化
table_name = "stockdb"
date_format = "YYYY-MM-DD"  # 你想要的日期格式
sql_query = f"insert into {table_name} values {}"
cursor.execute(sql_query)
# 獲取所有結果
results = cursor.fetchall()

# 在迴圈中處理結果
for row in results:
    print(row)


cursor.execute
# 提交變更
conn.commit()

# 關閉 cursor 和連線
cursor.close()
conn.close()
