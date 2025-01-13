import csv

data = {
    'company': [],
    'title': [],
    'description': [],
    'type': []
}

filename = 'american_jobs_classified.csv'
with open(filename, 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[3] not in {'Unknown', 'type'}:
            data['company'].append(row[0])
            data['title'].append(row[1])
            data['description'].append(row[2])
            data['type'].append(row[3])

job_type_count = {}
for job_type in data['type']:
    job_type_count[job_type] = job_type_count.get(job_type, 0) + 1

# count len of total jobs without unknown
total_jobs = len(data['type'])
for job_type, count in job_type_count.items():
    percentage = count / total_jobs * 100
    print(f'{job_type}: {percentage:.2f}%, {count} jobs')

# draw a bar chart
import matplotlib.pyplot as plt

plt.bar(job_type_count.keys(), job_type_count.values())
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.4)
plt.title('Job Type Distribution')
plt.ylabel('Number of Jobs')
plt.xlabel('Job Type')
plt.show()
