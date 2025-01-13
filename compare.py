import json
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

client = OpenAI(api_key="")

def create_embeddings(texts, model="text-embedding-ada-002"):
    """
    Create text embeddings using OpenAI
    """
    try:
        if not texts:
            return []
            
        # Ensure texts are strings
        texts = [str(text).strip() for text in texts if text]
        
        # Skip empty texts
        if not texts:
            return []
            
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
        print(f"Error creating embeddings: {e}")
        return []

def calculate_skills_similarity(jobs, user_skills):
    """
    Calculate similarity between user skills and job skills
    """
    try:
        # Create user skills embedding
        user_skills_list = [user_skills]  # Wrap in list to ensure 2D array
        user_embeddings = create_embeddings(user_skills_list)
        
        if not user_embeddings:
            raise ValueError("Failed to create user skills embeddings")

        # Extract job skills and create embeddings
        job_skills = [" ".join(job["skills"]) for job in jobs if job.get("skills")]
        job_embeddings = create_embeddings(job_skills)
        
        if not job_embeddings:
            raise ValueError("Failed to create job skills embeddings")

        # Ensure proper shape for cosine similarity
        user_embedding_array = [user_embeddings[0]]  # Reshape to 2D array
        
        # Calculate similarities
        similarities = cosine_similarity(user_embedding_array, job_embeddings)[0]
        
        # Add similarity scores to jobs
        jobs_with_similarity = []
        for i, job in enumerate(jobs):
            if i < len(similarities):  # Ensure we have a similarity score
                job_copy = job.copy()
                job_copy["similarity"] = float(similarities[i])
                jobs_with_similarity.append(job_copy)
        
        # Sort by similarity
        return sorted(jobs_with_similarity, key=lambda x: x["similarity"], reverse=True)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return []

def recommend_jobs(jobs, user_skills):
    """
    Recommend top 5 relevant jobs based on user skills
    """
    try:
        similar_jobs = calculate_skills_similarity(jobs, user_skills)
        
        recommendations = []
        for job in similar_jobs[:5]:
            recommendations.append({
                "company": job.get("company", "Unknown"),
                "title": job.get("title", "Unknown"),
                "similarity": job.get("similarity", 0.0),
                "skills": job.get("skills", [])  # Added to show required skills
            })
        
        return recommendations
    except Exception as e:
        print(f"Error recommending jobs: {e}")
        return []

def main():
    try:
        # Load JSON data
        with open('american_jobs_classified_no_model.json', 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        # Get user skills
        user_skills = input("Please enter your skills, separated by commas: ").strip()
        
        if not user_skills:
            print("No skills entered. Please provide at least one skill.")
            return
            
        # Get recommendations
        recommendations = recommend_jobs(jobs, user_skills)
        
        if not recommendations:
            print("No matching jobs found. Please try with different skills.")
            return
            
        # Display recommendations
        print("\nBased on your skills, here are the most suitable jobs:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. Company: {rec['company']}")
            print(f"   Position: {rec['title']}")
            print(f"   Match Score: {rec['similarity']:.2%}")
            print(f"   Required Skills: {', '.join(rec['skills'])}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()