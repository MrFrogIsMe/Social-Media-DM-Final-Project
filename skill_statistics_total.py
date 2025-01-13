import json
from collections import Counter
import matplotlib.pyplot as plt

# 讀取原始 JSON 檔案
with open("american_jobs_classified_no_model.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# 篩選 skills 不為空的資料
filtered_data = [job for job in data if job["skills"]]

# 將篩選結果保存到新檔案
with open("filtered_jobs.json", "w", encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4)

# 統計技能需求
skill_counter = Counter()
for job in filtered_data:
    skill_counter.update(job["skills"])

# 去除出現次數最高的技能
if skill_counter:
    highest_skill = skill_counter.most_common(1)[0][0]
    del skill_counter[highest_skill]

# 繪製技能需求統計圖（取前10個技能）
top_skills = skill_counter.most_common(10)
skills, counts = zip(*top_skills) if top_skills else ([], [])

plt.figure(figsize=(10, 6))
plt.bar(skills, counts, color='skyblue')
plt.xlabel("Skills")
plt.ylabel("Counts")
plt.title("Top 10 Skills in Job Listings")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("top_skills_chart.png")
plt.show()

print("篩選完成，結果儲存到 filtered_jobs.json")
print("技能統計圖儲存為 top_skills_chart.png")
