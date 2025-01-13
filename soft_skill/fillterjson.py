import json

# 讀取原始 JSON 檔案
input_file = './soft_skills_statistics.json'  # 請將這裡替換為你的 JSON 檔案名稱
output_file = 'filtered_soft_skills_statistics.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 過濾數值小於 10 的項目
filtered_data = {key: value for key, value in data.items() if value >= 100}

# 將過濾後的數據寫入新的 JSON 檔案
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4, ensure_ascii=False)

print(f"已成功將數值小於 100 的項目過濾，結果存儲於 {output_file}")
