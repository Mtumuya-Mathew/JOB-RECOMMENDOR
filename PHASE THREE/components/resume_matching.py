import streamlit as st
import PyPDF2
import docx
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import torch
from transformers import BertTokenizer, BertModel, pipeline

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", 
                        tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english")
st.write("Transformers loaded successfully.")

# Functions for resume extraction
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text):
    try:
        # Load the skills from the CSV file
        skills_df = pd.read_csv("data/skills.csv", header=None)  # No column names initially
        if skills_df.empty:
            raise ValueError("The skills CSV file is empty.")

        # Convert the single row of skills to a list (assuming skills are in a single row)
        skills_list = skills_df.iloc[0].dropna().tolist()  # Drop NaN values and convert to list

        # Clean up the list by stripping whitespace and converting to lowercase
        skills_list = [skill.strip().lower() for skill in skills_list]

    except FileNotFoundError:
        # Fallback to a default skill list if the file is missing
        skills_list = ["python", "java", "javascript", "sql", "excel", "machine learning", "reactjs"]
        print("Skills dataset file not found. Using default skills list.")
    except Exception as e:
        # Handle any other errors (e.g., empty CSV, unexpected format)
        skills_list = []
        print(f"Error reading skills file: {e}")

    # Extract and return skills found in the input text
    return [skill for skill in skills_list if skill in text]

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def compute_similarity_bert(text1, text2):
    embeddings1 = get_bert_embeddings(text1)
    embeddings2 = get_bert_embeddings(text2)
    cosine_sim = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
    return cosine_sim.item() * 100

# Function to load and display job data
def load_and_display_jobs(file_path):
    # Load CSV file using pandas
    
        # Reading the CSV file
        df = pd.read_csv(file_path)

        # Display the dataframe as a table in the Streamlit app
        st.dataframe(df)
        return df
    

# Define your CSV file path
file_path = "data/data job posts.csv"  # Update with the correct file path

# Load and display jobs
job_df = load_and_display_jobs(file_path)

def recommend_jobs(user_skills):
    if job_df is None:
        return []

    job_df['JobDescription'] = job_df['JobDescription'].fillna("")
    job_descriptions = job_df['JobDescription'].tolist()

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(job_descriptions + [user_skills])

    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    top_jobs = cosine_sim[0].argsort()[-5:][::-1]  # Get top 3 matching jobs

    recommended_jobs = []
    for idx in top_jobs:
        recommended_jobs.append({
            "title": job_df.iloc[idx]["Title"],
            "company": job_df.iloc[idx]["Company"],
            "location": job_df.iloc[idx]["Location"],
            "JobDescription": job_df.iloc[idx]["JobDescription"]
        })
    return recommended_jobs
def display_recommended_jobs(recommended_jobs):
    if not recommended_jobs:
        st.write("No recommendations found.")
        return
    
    st.write("### Recommended Jobs")
    
    # Loop through the recommended jobs in pairs
    for i in range(0, len(recommended_jobs), 2):
        cols = st.columns(2)  # Create two columns for each row
        for j, col in enumerate(cols):
            if i + j < len(recommended_jobs):  # Check if there's a job to display
                job = recommended_jobs[i + j]
                with col:
                    # Display job details as a card
                    st.write(
                        f"""
                        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; background-color: #f9f9f9; margin-bottom: 16px;">
                            <h4 style="margin: 0; color: #333;">{job['title']}</h4>
                            <p style="margin: 4px 0; color: #666;"><strong>Company:</strong> {job['company']}</p>
                            <p style="margin: 4px 0; color: #666;"><strong>Location:</strong> {job['location']}</p>
                            <p style="margin: 4px 0; color: #666;">{job['JobDescription'][:100]}...</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )



