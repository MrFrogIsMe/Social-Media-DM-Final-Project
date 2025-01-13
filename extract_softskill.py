from openai import OpenAI
import csv
import json
from collections import Counter, defaultdict

# Initialize OpenAI client
client = OpenAI(api_key="")

def extract_soft_skills(job_description):
    """
    Extracts soft skills from the job description using OpenAI API.
    """
    prompt = (
        f"Extract the key soft skills (e.g., communication, teamwork, problem-solving, adaptability) "
        f"from the following job description. Please list the soft skills separated by commas:\n\n"
        f"{job_description}\n\nSoft Skills (comma-separated):"
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts soft skills from job descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    # Extract the soft skills list from the response
    soft_skills = response.choices[0].message.content.strip().split(', ')
    return soft_skills

def explain_soft_skills(soft_skills):
    """
    Explains the categories or meaning of the extracted soft skills using OpenAI API.
    """
    skills_str = ', '.join(soft_skills)
    prompt = (
        f"Classify or explain the following soft skills based on their meaning or category: {skills_str}.\n\n"
        f"Provide detailed explanations for each skill in a list format, including their importance in professional settings."
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that classifies and explains soft skills."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()

# Read job data from CSV file and process
jobs = []
all_soft_skills = []
type_soft_skills = defaultdict(list)  # Dictionary to store soft skills grouped by type
with open('./few_american_jobs_classified.csv', 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
    reader = csv.DictReader(file)
    for row in reader:
        company = row['company']
        title = row['title']
        description = row['description']
        job_type = row['type']  # Read the 'type' column
        
        try:
            # Extract soft skills using OpenAI API
            soft_skills = extract_soft_skills(description)
            all_soft_skills.extend(soft_skills)  # Collect all skills for later statistics
            type_soft_skills[job_type].extend(soft_skills)  # Group skills by type
            
            # Add job data and extracted soft skills to the list
            jobs.append({
                "company": company,
                "title": title,
                "description": description,
                "type": job_type,  # Include job type in the output
                "soft_skills": soft_skills
            })
            print(f"Successfully processed job from {company}")
            
        except Exception as e:
            print(f"Error processing job from {company}: {str(e)}")

# Count the frequency of each soft skill
soft_skills_count = Counter(all_soft_skills)

# Count the frequency of soft skills per type
type_soft_skills_count = {job_type: Counter(skills) for job_type, skills in type_soft_skills.items()}

# Save processed job data to a JSON file
with open('jobs_with_soft_skills.json', 'w', encoding='utf-8') as json_file:
    json.dump(jobs, json_file, indent=4, ensure_ascii=False)  # Ensure non-ASCII characters are properly handled

# Prepare explanations and statistical data
unique_soft_skills = list(soft_skills_count.keys())
explanations = explain_soft_skills(unique_soft_skills)

# Save statistical data to a JSON file
with open('soft_skills_statistics.json', 'w', encoding='utf-8') as stats_file:
    json.dump(dict(soft_skills_count), stats_file, indent=4, ensure_ascii=False)

# Save type-based statistical data to a JSON file
with open('type_soft_skills_statistics.json', 'w', encoding='utf-8') as type_stats_file:
    json.dump(type_soft_skills_count, type_stats_file, indent=4, ensure_ascii=False)

# Save detailed explanations to a TXT file
with open('soft_skills_explanations.txt', 'w', encoding='utf-8') as explanations_file:
    explanations_file.write("Detailed Explanations of Soft Skills:\n\n")
    explanations_file.write(explanations)

print("Soft skills extraction completed.")
print("Detailed analysis saved to 'soft_skills_statistics.json', 'type_soft_skills_statistics.json', and 'soft_skills_explanations.txt'.")
