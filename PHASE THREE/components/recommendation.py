import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample job data (This would come from a real database in production)
job_data = [
    {"title": "Software Engineer - Python","company":"abc","location":"Kisii", "description": "Develop and maintain software using Python."},
    {"title": "Data Scientist - Machine Learning","company":"AMC","location":"Nairobi", "description": "Analyze data and create predictive models using Machine Learning techniques."},
    {"title": "Web Developer - ReactJS","company":"QLM","location":"Nairobari", "description": "Build web applications using ReactJS and JavaScript."}
]
job_df = pd.DataFrame(job_data)

def recommend_jobs(user_skills, user_experience):
    """
    Recommend jobs based on user's skills and experience using NLP-based job matching.
    """
    # Step 1: Combine the job descriptions into one string for vectorization
    job_descriptions = job_df['description'].tolist()

    # Step 2: Vectorize job descriptions and user skills using TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(job_descriptions + [user_skills])

    # Step 3: Calculate the cosine similarity between user skills and job descriptions
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Step 4: Get top matching jobs
    top_jobs = cosine_sim[0].argsort()[-3:][::-1]  # Get top 3 matching jobs

    recommended_jobs = []
    for idx in top_jobs:
        recommended_jobs.append({
    "title": job_df.iloc[idx]["title"],
    "company": job_df.iloc[idx]["company"],
    "location": job_df.iloc[idx]["location"],
    "description": job_df.iloc[idx]["description"]
})


    return recommended_jobs

# Example usage
user_skills = "Python, Machine Learning"
user_experience = "2 years"
recommended_jobs = recommend_jobs(user_skills, user_experience)
print("Recommended Jobs:", recommended_jobs)
