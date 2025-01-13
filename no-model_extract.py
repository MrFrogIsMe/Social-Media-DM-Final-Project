import csv
import json
import re

# 定義技術關鍵字
tech_keywords = {
    # 程式語言
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby", "swift", 
    "php", "kotlin", "r", "perl", "c", 

    # 資料庫與查詢語言
    "sql", "mysql", "postgresql", "mongodb", "redis", "firebase", "elasticsearch", 
    "graphql", "cassandra", "hive", "hbase", 

    # 雲端與基礎設施
    "aws", "azure", "google cloud", "gcp", "ibm cloud", "oracle cloud", "terraform", 
    "ansible", "cloudflare", "openstack", 

    # 容器與編排
    "docker", "kubernetes", "helm", "rancher", "nomad", 

    # 前端框架與工具
    "react", "angular", "vue", "svelte", "jquery", "next.js", "nuxt.js", "tailwind css", 
    "bootstrap", "sass", "less", 

    # 後端框架與工具
    "spring", "django", "flask", "express", "fastapi", "nestjs", "ruby on rails", "laravel", 
    "asp.net", "hapi", 

    # 資料科學與 AI
    "machine learning", "deep learning", "ai", "data science", "nlp", 

    # 數據工程與分析
    "etl", "data pipeline", "bigquery", "snowflake", 

    # 雲端 AI 工具
    "azure machine learning", "aws sagemaker", "google vertex ai", 

    # DevOps 與 CI/CD 工具
    "jenkins", "circleci", "travis ci", "github actions", "gitlab ci", "argo cd", 

    # 測試工具
    "selenium", "cypress", "junit", "pytest", "mocha", "chai", 

    # 版本控制與協作
    "git", "github", "gitlab", "bitbucket", "svn", 

    # 網路安全
    "penetration testing", "owasp", "kali linux", "metasploit", "wireshark", 

    # 大數據與分散式系統
    "hadoop", "spark", "kafka", "flink", "beam", "dask", "presto", 

    # 文書處理工具
    "excel", "word", "powerpoint", 

    # 其他
    "blockchain", "ethereum", "solidity", "smart contracts", "robotics", "edge computing", 
    "iot", "augmented reality", "virtual reality", "game development", "unity", "unreal engine"
}

def extract_keywords(text):
    """從工作描述中提取關鍵技能"""
    skills = set()

    # 用正則表達式將所有標點符號替換為空格，除了 '+' 和 '#'
    text = re.sub(r'[^\w\s+#]', ' ', text)

    # 將文字轉為小寫，並分割為單詞列表
    words = text.lower().split()

    # 比對技術關鍵字
    for word in words:
        # 檢查單詞是否是技術關鍵字
        if word in tech_keywords:
            skills.add(word)
    
    return list(skills)

def main():
    # 讀取和處理工作資料
    jobs = []
    with open('american_jobs_classified.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            company = row['company']
            title = row['title']
            description = row['description']
            type = row['type']
            
            try:
                # 提取技術技能
                skills = extract_keywords(description)
                
                # 添加工作資料和提取的技能
                jobs.append({
                    "company": company,
                    "title": title,
                    "skills": skills,
                    "type": type
                })
                print(f"成功處理 {company} 的工作資料")
                
            except Exception as e:
                print(f"處理 {company} 的工作資料時發生錯誤: {str(e)}")

    # 將處理後的資料儲存為 JSON
    with open('american_jobs_classified_no_model.json', 'w', encoding='utf-8') as json_file:
        json.dump(jobs, json_file, indent=4, ensure_ascii=False)

    print("技能提取完成並儲存至 'jobs_with_skills.json'")

if __name__ == "__main__":
    main()
