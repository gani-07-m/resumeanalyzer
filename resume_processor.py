import random

def calculate_ats_score(resume_text, job_description):
    return round(random.uniform(50, 100), 2)  # Replace with real NLP scoring logic

def update_resume(resume_text, job_description):
    return f"{resume_text}\n\n[Updated based on JD: {job_description}]"
