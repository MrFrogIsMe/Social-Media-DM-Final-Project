from openai import OpenAI
import csv
import json

# Initialize OpenAI client
client = OpenAI(api_key="")

def extract_keywords(job_description):
    """Extracts keywords from the job description using OpenAI API."""
    prompt = f"Extract the key technical skills (e.g., Python, SQL, C++) from the following job description. Please list the skills separated by commas:\n\n{job_description}\n\nSkills (comma-separated):"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts technical skills from job descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    # Extract the skills list from the response
    skills = response.choices[0].message.content.strip().split(', ')
    return skills

# Read job data from CSV file and process
jobs = []
with open('jobs.csv', 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
    reader = csv.DictReader(file)
    for row in reader:
        company = row['company']
        title = row['title']
        description = row['description']
        
        try:
            # Extract technical skills using OpenAI API
            skills = extract_keywords(description)
            
            # Add job data and extracted skills to the list
            jobs.append({
                "company": company,
                "title": title,
                "skills": skills
            })
            print(f"Successfully processed job from {company}")
            
        except Exception as e:
            print(f"Error processing job from {company}: {str(e)}")

# Save processed data to a JSON file
with open('jobs_with_skills_4omini.json', 'w', encoding='utf-8') as json_file:
    json.dump(jobs, json_file, indent=4, ensure_ascii=False)  # Ensure non-ASCII characters are properly handled

print("Skills extraction completed and saved to 'jobs_with_skills.json'")