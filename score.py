def calculate_field_score(user_skills, job_data, soft_skills, user_soft_skills):
    """
    Calculate scores for different fields based on missing skills, their frequencies, and soft skill bonuses.
    
    Args:
    user_skills (list): List of user's skills in lowercase
    job_data (list): List of job types and their required skills
    soft_skills (dict): Dictionary of soft skills and their frequency
    user_soft_skills (list): List of user's soft skills
    
    Returns:
    dict: Scores for each job field (0-10) with possible bonus for soft skills
    """
    
    # Convert user skills to lowercase for case-insensitive matching
    user_skills = [skill.lower().strip() for skill in user_skills]
    
    field_scores = {}
    
    for job_type in job_data:
        job_title = job_type['type']
        if job_title == 'Unknown' or job_title == 'Intern':  # Skip unknown job types
            continue
            
        # Get all skills for this job type and their frequencies
        job_skills = job_type['skills']
        total_positions = job_type['total']
        
        if total_positions == 0:
            continue
            
        # Start with perfect score
        score = 10.0
        
        # Calculate total mentions for percentage calculation
        total_mentions = sum(job_skills.values())
        
        # Sort skills by frequency (highest to lowest)
        sorted_skills = sorted(job_skills.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate penalties for missing skills
        for skill, frequency in sorted_skills:
            if skill.lower() not in user_skills:
                frequency_percentage = (frequency / total_mentions) * 100
                
                if frequency_percentage > 20:
                    penalty = 1.5 + (frequency_percentage) / 20
                elif frequency_percentage > 10:
                    penalty = 0.3 + (frequency_percentage - 10) / 10
                elif frequency_percentage > 5:
                    penalty = 0.2 + (frequency_percentage - 5) / 10
                else:
                    penalty = 0.0 + frequency_percentage / 10
                
                score -= penalty
        
        # Soft skills bonus: Increase score if user has matching soft skills
        soft_skill_bonus = 0
        for soft_skill in user_soft_skills:
            if soft_skill in soft_skills:
                # Frequency-based bonus: 0.1 to 0.3
                skill_frequency = soft_skills[soft_skill]
                if skill_frequency >= 1500:
                    soft_skill_bonus += 0.3  # Highly frequent soft skill
                elif skill_frequency >= 1000:
                    soft_skill_bonus += 0.2  # Moderately frequent soft skill
                else:
                    soft_skill_bonus += 0.1  # Less frequent soft skill

        # Apply soft skill bonus
        score += soft_skill_bonus
        
        # Ensure score doesn't go above 10 and is not negative
        field_scores[job_title] = max(min(round(score, 1), 10), 0)
    
    return field_scores

def get_skill_assessment(user_skills_input, user_soft_skills_input, job_data, soft_skills_data):
    """
    Get a comprehensive skill assessment with missing skills analysis and soft skills boost
    
    Args:
    user_skills_input (str): Comma-separated string of user skills
    user_soft_skills_input (str): Comma-separated string of user soft skills
    job_data (list): Job market data
    soft_skills_data (dict): Soft skills data
    
    Returns:
    dict: Assessment results including scores, recommendations, and soft skill impact
    """
    # Split and clean user input
    user_skills = [s.strip() for s in user_skills_input.split(',')]
    user_soft_skills = [s.strip().lower() for s in user_soft_skills_input.split(',')]
    
    # Calculate scores for each field, considering both hard and soft skills
    field_scores = calculate_field_score(user_skills, job_data, soft_skills_data, user_soft_skills)
    
    # Sort fields by score
    sorted_fields = sorted(field_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Get missing critical skills for top fields
    missing_critical_skills = {}
    for field, _ in sorted_fields[:3]:
        for job_type in job_data:
            if job_type['type'] == field:
                top_skills = sorted(job_type['skills'].items(), key=lambda x: x[1], reverse=True)[:5]
                missing = [skill for skill, freq in top_skills if skill.lower() not in [s.lower() for s in user_skills]]
                if missing:
                    missing_critical_skills[field] = missing
    
    # Prepare assessment results
    assessment = {
        'scores': field_scores,
        'top_fields': [field for field, score in sorted_fields[:3]],
        'average_score': round(sum(field_scores.values()) / len(field_scores), 1),
        'strongest_field': sorted_fields[0][0],
        'strongest_score': sorted_fields[0][1],
        'missing_critical_skills': missing_critical_skills
    }
    
    return assessment

# Example usage
if __name__ == "__main__":
    import json
    
    try:
        with open('type_skill_stats.json', 'r', encoding='utf-8') as f:
            job_data = json.load(f)
        
        # Soft skills data from your provided file
        soft_skills_data = {
            "communication": 1505,
            "teamwork": 1473,
            "problem-solving": 1434,
            "adaptability": 1538,
            "attention to detail": 676,
            "analytical thinking": 106,
            "collaboration": 526,
            "interpersonal skills": 234,
            "organizational skills": 181,
            "customer service": 219,
            "empathy": 182,
            "initiative": 117,
            "creativity": 201,
            "reliability": 121,
            "time management": 284,
            "organization": 190,
            "flexibility": 283,
            "self-motivation": 104,
            "willingness to learn": 137,
            "leadership": 187
        }
        
        user_skills_input = input("請輸入您的技能，用逗號分隔（例如：python, java, sql）：")
        user_soft_skills_input = input("請輸入您的軟實力技能，用逗號分隔（例如：communication, teamwork, adaptability）：")
        
        assessment = get_skill_assessment(user_skills_input, user_soft_skills_input, job_data, soft_skills_data)
        
        print("\n=== 技能評估結果 ===")
        print("\n各領域分數（滿分10分）：")
        for field, score in sorted(assessment['scores'].items(), key=lambda x: x[1], reverse=True):
            print(f"{field}: {score}/10")
            
        print(f"\n整體平均分數：{assessment['average_score']}/10")
        print(f"最強領域：{assessment['strongest_field']} ({assessment['strongest_score']}/10)")
        
        print("\n最適合的三個領域：")
        for field in assessment['top_fields']:
            print(f"\n- {field}")
            if field in assessment['missing_critical_skills']:
                print("  建議加強的關鍵技能：")
                for skill in assessment['missing_critical_skills'][field]:
                    print(f"  * {skill}")
            
    except Exception as e:
        print(f"發生錯誤：{e}")
