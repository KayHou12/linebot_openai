import pandas as pd

# 創建一個範例 DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

# 顯示原始 DataFrame
print("原始 DataFrame:")
print(df)

# 移除索引
df_reset = df.reset_index(drop=True)

# 顯示移除索引後的 DataFrame
print("\n移除索引後的 DataFrame:")
print(df_reset)
