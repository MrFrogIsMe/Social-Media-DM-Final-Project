import json

# 讀取原始 JSON 檔案
input_file = './type_soft_skills_statistics.json'  # 替換為你的檔案名稱
output_file = 'filtered_type_soft_skills_statistics.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 遍歷所有 type，過濾數值小於 50 的項目
filtered_data = {
    job_type: {key: value for key, value in skills.items() if value >= 50}
    for job_type, skills in data.items()
}

# 將過濾後的數據寫入新的 JSON 檔案
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4, ensure_ascii=False)

print(f"已成功過濾數值小於 50 的項目，結果存儲於 {output_file}")
