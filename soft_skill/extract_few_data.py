import csv

# 原始檔案名稱
input_file = './american_jobs_classified.csv'
# 新檔案名稱
output_file = './few_american_jobs_classified.csv'

# 讀取原始檔案並取前五筆資料
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # 讀取標題列
    rows = [header] + [next(reader) for _ in range(5)]  # 取前五筆資料

# 寫入新檔案
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)

print(f"前五筆資料已成功儲存至 {output_file}")
