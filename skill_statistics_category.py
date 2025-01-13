import json
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

# 讀取篩選後的資料
with open("filtered_jobs.json", "r", encoding='utf-8') as file:
    filtered_data = json.load(file)

# 初始化一個字典來儲存統計結果
type_skill_stats = defaultdict(lambda: {"total": 0, "skills": Counter()})

# 統計各個type的技能需求以及總工作數量
for job in filtered_data:
    job_type = job["type"]
    job_skills = job["skills"]
    
    # 更新該type的工作數量
    type_skill_stats[job_type]["total"] += 1
    
    # 更新該type的技能需求
    type_skill_stats[job_type]["skills"].update(job_skills)

# 格式化輸出為所需格式
result = []
for job_type, stats in type_skill_stats.items():
    result.append({
        "type": job_type,
        "total": stats["total"],
        "skills": dict(stats["skills"])
    })

# 輸出到新檔案
with open("type_skill_stats.json", "w", encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print("統計結果已儲存至 type_skill_stats.json")

# 為每個type畫出技能統計圖
for job_type, stats in type_skill_stats.items():
    skills, counts = zip(*stats["skills"].items())  # 取得技能與其對應的次數

    # 畫出圖表
    plt.figure(figsize=(10, 6))
    plt.bar(skills, counts, color='skyblue')
    plt.xlabel("Skills")
    plt.ylabel("Counts")
    plt.title(f"Skills Demand for {job_type}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # 儲存圖表為 PNG 檔案
    chart_filename = f"skills_demand_{job_type.replace('/', '_')}.png"
    plt.savefig(chart_filename)
    plt.close()  # 關閉圖表以便繪製下一張

    print(f"圖表已儲存為 {chart_filename}")

print("所有圖表已儲存")
