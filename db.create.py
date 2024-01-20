import psycopg2
from psycopg2 import sql

# 建立資料庫連線
conn = psycopg2.connect(
    host="dpg-cmj44gocmk4c739n03bg-a.oregon-postgres.render.com",
    user="db_4qcx_user db_4qcx",
    password="diKiHADHIiXgWkRa8TrxA57mQt07Jx23",
    database="db_4qcx"
)

# 建立一個 cursor 物件
cursor = conn.cursor()
table_name = "stockdb"

# 建立資料表
create_table_query = sql.SQL("""
    CREATE TABLE {} (
        stock_n VARCHAR(255),
        Date DATE,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        "Adj Close" FLOAT,
        Volume FLOAT,
        PRIMARY KEY (stock_n, Date)
    )
""").format(sql.Identifier(table_name))

# 執行 SQL 語句
cursor.execute(create_table_query)

# 提交變更
conn.commit()

# 關閉 cursor 和連線
cursor.close()
conn.close()


