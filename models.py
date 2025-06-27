from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # student or recruiter

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    original_path = db.Column(db.String(200))
    updated_path = db.Column(db.String(200))
    ats_score = db.Column(db.Float)
    job_description = db.Column(db.Text)
