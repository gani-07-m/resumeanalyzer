from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from models import User, Resume
import os
from werkzeug.utils import secure_filename
from resume_processor import calculate_ats_score, update_resume

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join('app', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            role=request.form['role']
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password, role=role).first()
        
        if user:
            session['user_id'] = user.id
            session['role'] = role
            return redirect(url_for('main.recruiter_dashboard' if role == 'recruiter' else 'main.student_dashboard'))
        else:
            flash("Invalid credentials. Try again.", "error")  # <-- Flash message here

    return render_template('login.html')


@main.route('/recruiter_dashboard', methods=['GET', 'POST'])
def recruiter_dashboard():
    results = []
    if request.method == 'POST':
        jd = request.form['jd']
        score_threshold = float(request.form['threshold'])
        uploaded_files = request.files.getlist('resumes')

        for file in uploaded_files:
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            # Read file content as plain text (works only for .txt or .docx if converted)
            try:
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                content = ""
                print(f"Error reading file {filename}: {e}")

            score = calculate_ats_score(content, jd)
            if score >= score_threshold:
                results.append((filename, score))

    return render_template('recruiter_dashboard.html', results=results)

@main.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    score = None
    updated = None
    if request.method == 'POST':
        jd = request.form['jd']
        resume = request.files['resume']
        filename = secure_filename(resume.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        resume.save(path)

        try:
            with open(path, 'r', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            content = ""
            print(f"Error reading file: {e}")

        score = calculate_ats_score(content, jd)
        updated = update_resume(content, jd)

    return render_template('student_dashboard.html', score=score, updated_resume=updated)
