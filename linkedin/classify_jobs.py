import re
import csv
import pandas as pd

job_types = {
    "AI/Machine Learning Engineer": ["AI", "Machine Learning", "ML", "Deep Learning", "NLP", "Data Scientist"],
    "Cybersecurity Engineer": ["Cybersecurity", "Security", "Penetration Testing", "SOC"],
    "Devops Engineer": ["DevOps", "CI/CD", "Kubernetes", "Docker", "Cloud Infrastructure"],
    "Full-Stack Developer": ["Full Stack", "Frontend", "Backend", "React", "Angular", "Node.js"],
    "Software Architect": ["Software Architect", "Solution Architect", "System Design"],
    "Cloud Architect": ["Cloud Architect", "AWS", "Azure", "GCP"],
    "Data Scientist": ["Data Scientist", "Data Analysis", "Statistical Modeling", "Big Data"],
    "Software Engineer": ["Software Engineer", "Developer", "Programming", "Coding"],
    "IT Project Manager": ["IT Project Manager", "Scrum Master", "Agile", "Project Management"],
    "IOT Engineer": ["IoT", "Internet of Things", "Embedded Systems", "Edge Computing"],
    "UI/UX Designers": ["UI/UX Designer", "User Experience", "User Interface", "Interaction Design"],
    "Intern": ["Intern", "Internship", "Trainee"],
    "Unknown": [""]
}

def classify_job(title, description):
    for job_type, keywords in job_types.items():
        for keyword in keywords:
            if re.search(rf'\b{keyword}\b', title, re.IGNORECASE) or \
               re.search(rf'\b{keyword}\b', description, re.IGNORECASE):
                return job_type
    return "Unknown"

data = {
    'company': [],
    'title': [],
    'description': [],
    'type': []
}

filename = 'american_jobs_plus.csv'
with open(filename, 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        data['company'].append(row[0])
        data['title'].append(row[1])
        data['description'].append(row[2])


# 將工作分類
classified_jobs = []
for title, description in zip(data['title'], data['description']):
    job_type = classify_job(title, description)
    classified_jobs.append(job_type)
    data['type'].append(job_type)
    print(f'{job_type} - {title}')

# 結果輸出
# for job in classified_jobs:
#     print(job)

# print percentage of each job type
job_type_count = {}
for job_type in job_types.keys():
    job_type_count[job_type] = 0

for job_type in classified_jobs:
    job_type_count[job_type] += 1

total_jobs = len(classified_jobs)
for job_type, count in job_type_count.items():
    percentage = count / total_jobs * 100
    print(f'{job_type}: {percentage:.2f}%, {count} jobs')

# df = pd.DataFrame(data)
# df.to_csv('american_jobs_classified.csv', index=False)
