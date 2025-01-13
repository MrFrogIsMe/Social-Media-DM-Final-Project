import matplotlib.pyplot as plt
import json

# Data for AI/Machine Learning Engineer
ai_ml_data = {
    "communication": 181,
    "teamwork": 173,
    "problem-solving": 180,
    "adaptability": 183,
    "attention to detail": 55,
    "collaboration": 131,
    "creativity": 65
}

# Data for Cybersecurity Engineer
cybersecurity_data = {
    "communication": 182,
    "teamwork": 180,
    "problem-solving": 183,
    "adaptability": 184,
    "attention to detail": 92,
    "collaboration": 79
}

# Function to plot bar charts
def plot_skills(data, title, filename):
    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.barh(categories, values, color="skyblue")

    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Soft Skills", fontsize=12)
    plt.title(title, fontsize=16)
    plt.tight_layout()

    # Save the plot
    plt.savefig(filename)

    # Show the plot
    plt.show()

# Plot for AI/Machine Learning Engineer
plot_skills(ai_ml_data, "Soft Skills for AI/Machine Learning Engineer", "ai_ml_skills_histogram.png")

# Plot for Cybersecurity Engineer
plot_skills(cybersecurity_data, "Soft Skills for Cybersecurity Engineer", "cybersecurity_skills_histogram.png")
