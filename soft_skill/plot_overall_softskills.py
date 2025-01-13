import matplotlib.pyplot as plt
import json

# Data from the JSON
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

# Extract keys and values
categories = list(soft_skills_data.keys())
values = list(soft_skills_data.values())

# Create the bar chart
plt.figure(figsize=(12, 8))
plt.barh(categories, values, color="skyblue")

# Add labels and title
plt.xlabel("Frequency", fontsize=12)
plt.ylabel("Soft Skills", fontsize=12)
plt.title("Soft Skills Frequency Distribution", fontsize=16)

# Improve layout
plt.tight_layout()
# Save the plot
plt.savefig("soft_skills_overall_histogram.png")
# Show the plot
plt.show()
