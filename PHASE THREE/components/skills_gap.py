# skills_gap.py

def analyze_gap(user_skills: str, target_job: str) -> tuple:
    """
    Analyzes the gap between user's skills and target job requirements.

    Args:
        user_skills (str): User's skills as a comma-separated string.
        target_job (str): Target job title.

    Returns:
        tuple: (missing_skills, recommendations)
    """
    # Placeholder data: Replace with actual skills database and comparison logic.
    required_skills = {
        "Data Scientist": ["Python", "Machine Learning", "SQL", "Statistics"],
        "Web Developer": ["HTML", "CSS", "JavaScript", "ReactJS"],
    }

    user_skills_list = [skill.strip().lower() for skill in user_skills.split(",")]
    target_skills = required_skills.get(target_job, [])
    missing_skills = [skill for skill in target_skills if skill.lower() not in user_skills_list]
    recommendations = [f"Learn {skill}" for skill in missing_skills]

    return missing_skills, recommendations
