import json
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

client = OpenAI(api_key="")

def create_embeddings(texts, model="text-embedding-ada-002"):
    """
    使用 OpenAI 創建文本嵌入
    """
    try:
        embeddings = []
        for i in range(0, len(texts), 50):
            batch = texts[i:i+50]
            response = client.embeddings.create(
                input=batch, 
                model=model
            )
            embeddings.extend([embed.embedding for embed in response.data])
        return embeddings
    except Exception as e:
        print(f"創建 embedding 時發生錯誤: {e}")
        return []

def calculate_skills_similarity(jobs, user_skills):
    """
    計算用戶技能與工作的技能相似度
    """
    # 創建用戶技能的嵌入
    user_skills_embedding = create_embeddings([user_skills])[0]
    
    # 提取每個工作的技能描述並創建嵌入
    job_skills = [" ".join(job["skills"]) for job in jobs]
    job_embeddings = create_embeddings(job_skills)
    
    # 計算相似度
    similarities = cosine_similarity([user_skills_embedding], job_embeddings)[0]
    
    # 添加相似度到每個工作
    for i, job in enumerate(jobs):
        job["similarity"] = similarities[i]
    
    # 根據相似度排序
    sorted_jobs = sorted(jobs, key=lambda x: x["similarity"], reverse=True)
    
    return sorted_jobs

def analyze_multiple_skills(jobs, user_skills_list):
    """
    分析多個用戶的技能與工作的相似度
    """
    results = {}
    for user_skills in user_skills_list:
        print(f"\n分析用戶技能: {user_skills}")
        similar_jobs = calculate_skills_similarity(jobs, user_skills)
        
        # 顯示前 5 個最相似的工作
        print("前 5 個最相似的工作：")
        user_results = []
        for job in similar_jobs[:5]:
            result = {
                "company": job["company"],
                "title": job["title"],
                "similarity": job["similarity"]
            }
            user_results.append(result)
            print(f"公司: {result['company']}")
            print(f"職位: {result['title']}")
            print(f"相似度: {result['similarity']:.4f}")
            print("----")
        
        results[user_skills] = user_results
    return results

# 使用範例
def main():
    # JSON 資料加載
    with open('job.json', 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    
    # 用戶技能列表
    user_skills_list = [
        "Python, machine learning, data analysis, cloud computing",
        "Marketing, SEO, digital advertising, content creation",
        "Project management, Agile methodologies, team leadership",
        "Data visualization, statistics, SQL, business intelligence"
    ]
    
    # 計算並分析多個用戶的技能相似度
    results = analyze_multiple_skills(jobs, user_skills_list)
    
    # 保存結果
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
