import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv('american_jobs_classified.csv')

# 計算行數
num_rows = len(df)
print(f'The number of rows in the CSV file is: {num_rows}')
