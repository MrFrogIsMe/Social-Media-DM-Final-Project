import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from typing import Dict, List, Tuple
import time
from tqdm import tqdm
import chardet
import re
from collections import defaultdict

# 設定 OpenAI API 金鑰
client = OpenAI(api_key= "")  
# 定義軟實力類別及描述
soft_skills_extended = {
    "親和力": {
        "description": "營造輕鬆氛圍，迅速與人拉近距離",
        "keywords": ["人際關係", "溝通", "友善", "親切", "和藹", "團隊合作", "社交能力", "親和力", "和善", "待人"],
        "context": ["customer service", "team environment", "interpersonal skills", "relationship building", "communication skills", "friendly", "approachable"]
    },
    "反應力": {
        "description": "敏銳理解言語和非言語訊息",
        "keywords": ["快速反應", "應變能力", "靈活", "敏銳", "觀察力", "臨機應變", "反應迅速"],
        "context": ["fast-paced", "dynamic environment", "quick response", "adaptability", "fast learner", "agile", "responsive"]
    },
    "語境理解力": {
        "description": "結合語境，快速理解對方的反應",
        "keywords": ["理解力", "洞察力", "觀察力", "語境掌握", "情境理解", "解讀能力"],
        "context": ["situational awareness", "context understanding", "perception", "emotional intelligence", "read between lines"]
    },
    "人脈開拓力": {
        "description": "有意識連結他人並發展關係",
        "keywords": ["人脈建立", "社交網絡", "關係維護", "交際能力", "拓展人脈", "建立關係"],
        "context": ["networking", "relationship building", "business development", "social networking", "connection building"]
    },
    "表達力": {
        "description": "簡潔清晰地表達自己的觀點和想法",
        "keywords": ["表達能力", "溝通技巧", "口語表達", "簡報能力", "說服力", "清晰表達"],
        "context": ["communication skills", "presentation skills", "public speaking", "articulate", "clear communication"]
    },
    "諮詢力": {
        "description": "以開放的姿態聆聽他人，建立信任的溝通關係",
        "keywords": ["諮詢技巧", "傾聽能力", "同理心", "建立信任", "開放態度", "溝通技巧"],
        "context": ["active listening", "consultation skills", "counseling", "advisory", "trustworthy communication"]
    },
    "談判力": {
        "description": "理解各方的利益訴求，有技巧地協商",
        "keywords": ["談判技巧", "協商能力", "說服力", "溝通技巧", "利益平衡", "折衷方案"],
        "context": ["negotiation skills", "deal-making", "conflict resolution", "mediation", "stakeholder management"]
    },
    "團隊協作": {
        "description": "能與他人合作，共同完成目標",
        "keywords": ["團隊合作", "協同合作", "配合", "互助", "團隊精神", "共同目標"],
        "context": ["team player", "collaborative", "cross-functional", "teamwork", "cooperation", "joint effort"]
    },
    "領導力": {
        "description": "得到他人的信任和尊重，帶領他人行動",
        "keywords": ["領導能力", "帶領團隊", "決策能力", "影響力", "統籌能力", "團隊管理"],
        "context": ["leadership", "team management", "decision making", "influence", "guidance", "strategic thinking"]
    },
    "委任力": {
        "description": "將工作安排給合適的人",
        "keywords": ["任務分配", "工作委派", "授權能力", "資源分配", "人員調度"],
        "context": ["delegation", "task assignment", "resource allocation", "work distribution", "responsibility sharing"]
    },
    "督導力": {
        "description": "能監督和評估他人的工作進度和質量",
        "keywords": ["監督能力", "績效評估", "品質控管", "進度管理", "考核能力"],
        "context": ["supervision", "performance monitoring", "quality control", "progress tracking", "evaluation"]
    },
    "傳授力": {
        "description": "能將自己的經驗技能傳授給他人",
        "keywords": ["教學能力", "知識傳遞", "經驗分享", "培訓能力", "指導技巧"],
        "context": ["training", "mentoring", "knowledge sharing", "coaching", "skill transfer", "teaching"]
    },
    "協同力": {
        "description": "促使不同利益方達成共識，統一目標",
        "keywords": ["協調能力", "整合能力", "共識建立", "目標統一", "利益平衡"],
        "context": ["coordination", "alignment", "consensus building", "stakeholder management", "synchronization"]
    },
    "組織力": {
        "description": "能獲取資源並有系統地整合、分配",
        "keywords": ["組織能力", "資源整合", "系統規劃", "資源分配", "規劃能力"],
        "context": ["organization skills", "resource management", "planning", "systematic approach", "coordination"]
    },
    "樂觀力": {
        "description": "正向思考，積極樂觀的工作態度",
        "keywords": ["正向思考", "積極態度", "樂觀", "正面能量", "積極進取"],
        "context": ["positive attitude", "optimistic", "enthusiasm", "positive mindset", "can-do attitude"]
    },
    "持續學習力": {
        "description": "在快節奏中也能不斷吸收新知識",
        "keywords": ["學習能力", "自我提升", "終身學習", "知識吸收", "進修意願"],
        "context": ["continuous learning", "self-improvement", "life-long learning", "growth mindset", "development"]
    },
    "目標發現力": {
        "description": "可以快速抓住關鍵目標並全力以赴",
        "keywords": ["目標設定", "重點掌握", "關鍵識別", "目標導向", "優先順序"],
        "context": ["goal setting", "target identification", "prioritization", "objective focus", "strategic thinking"]
    },
    "專業構築力": {
        "description": "展現自己在專業領域的專家地位",
        "keywords": ["專業能力", "專業發展", "領域專精", "專業知識", "技術精進"],
        "context": ["expertise", "professional development", "domain knowledge", "subject matter expert", "specialization"]
    },
    "適應力": {
        "description": "能快速適應新環境，容忍乃至歡迎變化",
        "keywords": ["適應能力", "變革管理", "彈性思維", "環境適應", "變通能力"],
        "context": ["adaptability", "change management", "flexibility", "resilience", "versatility"]
    },
    "分析力": {
        "description": "綜合訊息和觀點，做出可靠的推理",
        "keywords": ["分析能力", "邏輯思維", "資料分析", "問題分析", "推理能力"],
        "context": ["analytical skills", "logical thinking", "data analysis", "problem solving", "critical thinking"]
    },
    "批判力": {
        "description": "從正反兩面進行思考，做出權衡",
        "keywords": ["批判思考", "多角度思考", "辨析能力", "思辨能力", "判斷力"],
        "context": ["critical thinking", "evaluation", "reasoning", "objective analysis", "balanced judgment"]
    },
    "創意力": {
        "description": "產生奇思妙想，創造新產品、新設計、新想法",
        "keywords": ["創新能力", "創意思考", "創新思維", "發想能力", "創造力"],
        "context": ["creativity", "innovation", "original thinking", "ideation", "design thinking", "brainstorming"]
    },
    "判斷力": {
        "description": "在多個可能性中，迅速做出選擇並承擔結果",
        "keywords": ["決策能力", "判斷能力", "風險評估", "決斷力", "選擇力"],
        "context": ["decision making", "judgment", "risk assessment", "evaluation", "decisive action"]
    },
    "規劃力": {
        "description": "依據目標和需求，規劃多種可行方案",
        "keywords": ["規劃能力", "方案制定", "策略規劃", "計畫擬定", "目標規劃"],
        "context": ["planning", "strategic planning", "project planning", "roadmap development", "strategy formulation"]
    }
}

def detect_encoding(file_path: str) -> str:
    """
    自動檢測檔案的編碼格式
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    讀取 CSV 文件，使用檢測到的編碼
    """
    # 檢測編碼
    encoding = detect_encoding(file_path)
    print(f"檢測到的檔案編碼: {encoding}")
    return pd.read_csv(file_path, encoding=encoding)

def preprocess_text(text: str) -> str:
    """
    預處理文本
    """
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'\r\n|\n|\r', ' ', text)  # 處理換行符
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    return text

def get_embedding(text: str, model: str = "text-embedding-ada-002", max_retries: int = 3) -> List[float]:
    """
    獲取文本嵌入向量
    """
    for attempt in range(max_retries):
        try:
            response = client.embeddings.create(
                model=model,
                input=text[:8000]
            )
            return response.data[0].embedding
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error getting embedding: {str(e)}")
                raise
            time.sleep(2 ** attempt)

def calculate_keyword_score(text: str, skill_info: dict) -> float:
    """
    計算關鍵詞匹配分數
    """
    text = preprocess_text(text)
    
    # 計算關鍵詞出現次數
    keyword_matches = sum(1 for keyword in skill_info["keywords"] 
                         if keyword.lower() in text)
    
    # 計算上下文匹配次數
    context_matches = sum(1 for context in skill_info["context"] 
                         if context.lower() in text)
    
    # 計算加權分數
    total_keywords = len(skill_info["keywords"])
    total_context = len(skill_info["context"])
    
    # 避免除以零
    if total_keywords == 0 or total_context == 0:
        return 0.0
    
    keyword_score = keyword_matches / total_keywords * 0.8
    context_score = context_matches / total_context * 0.1
    
    return min(keyword_score + context_score, 1.0)

def analyze_job_posting(
    description: str,
    skill_embeddings: Dict[str, List[float]],
    threshold: float = 0.3
) -> Tuple[List[Dict], Dict[str, float]]:
    """
    分析單個職位描述
    """
    try:
        processed_text = preprocess_text(description)
        if not processed_text:
            return [], {}
        
        # 獲取職位描述的嵌入向量
        description_embedding = get_embedding(processed_text)
        
        # 計算每個軟實力的分數
        skill_scores = {}
        for skill, skill_info in soft_skills_extended.items():
            # 計算嵌入向量相似度
            embedding_similarity = float(cosine_similarity(
                [description_embedding], 
                [skill_embeddings[skill]]
            )[0][0])
            
            # 計算關鍵詞匹配分數
            keyword_score = calculate_keyword_score(processed_text, skill_info)
            
            # 計算最終分數（結合兩種分數）
            final_score = embedding_similarity * 0.4 + keyword_score * 0.6
            skill_scores[skill] = final_score
        
        # 找出分數最高的技能
        sorted_skills = sorted(
            skill_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # 使用動態閾值
        scores = [score for _, score in sorted_skills]
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        dynamic_threshold = max(threshold, mean_score + 0.5 * std_score)
        
        # 篩選出顯著的技能
        significant_skills = [
            {
                "skill": skill,
                "score": score,
                "keywords": soft_skills_extended[skill]["keywords"],
                "context": soft_skills_extended[skill]["context"]
            }
            for skill, score in sorted_skills
            if score > dynamic_threshold
        ]
        
        return significant_skills, skill_scores
        
    except Exception as e:
        print(f"分析過程中發生錯誤: {str(e)}")
        return [], {}

def main():
    try:
        # 讀取職缺資料
        print("讀取職缺資料...")
        file_path = './jobs.csv'
        data = read_csv_file(file_path)
        
        # 初始化軟實力嵌入向量
        print("初始化軟實力嵌入向量...")
        skill_embeddings = {}
        for skill, info in tqdm(soft_skills_extended.items()):
            try:
                skill_embeddings[skill] = get_embedding(
                    info["description"] + " " + " ".join(info["keywords"])
                )
            except Exception as e:
                print(f"無法獲取 {skill} 的嵌入向量: {str(e)}")
        
        # 分析所有職位
        results = []
        print("開始分析職缺描述...")
        for _, row in tqdm(data.iterrows(), total=len(data)):
            try:
                significant_skills, all_scores = analyze_job_posting(
                    row['description'],
                    skill_embeddings
                )
                
                if significant_skills:
                    result = {
                        "company": row['company'],
                        "title": row['title'],
                        "significant_skills": significant_skills,
                        "all_skill_scores": all_scores
                    }
                    results.append(result)
                
            except Exception as e:
                print(f"處理職缺時發生錯誤 ({row['company']} - {row['title']}): {str(e)}")
                continue
        
        # 轉換結果為更易讀的格式
        # 替換 main 函數中結果轉換和保存部分
        formatted_results = []
        for result in results:
            row = {
                "company": result["company"],
                "title": result["title"]
            }
            for skill, score in result["all_skill_scores"].items():
                # 根據分數 >= 0.3 判斷是否填入 1 或 0
                row[f"{skill}(1 or 0)"] = 1 if score >= 0.3 else 0
                row[f"{skill}(分數)"] = score
            formatted_results.append(row)

        # 保存結果為 CSV
        output = pd.DataFrame(formatted_results)
        output.to_csv(
            "classified_soft_skills_results.csv",
            index=False,
            encoding="utf-8-sig"
        )
        print("分類完成，結果已保存到 classified_soft_skills_results.csv")

        
        # 輸出一些統計信息
        print("\n分析統計：")
        print(f"總共分析的職位數量: {len(data)}")
        print(f"檢測到軟實力的職位數量: {len(results)}")
        print(f"檢測率: {len(results)/len(data)*100:.2f}%")
        
    except Exception as e:
        print(f"程式執行過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()