import os
from flask import Blueprint, request, jsonify, send_file, render_template_string
from .cv_model import CV
from .school_model import School
from .workexperience_model import WorkExperience
from .project_model import Project
from app.auth import User
from app.database import db
import pdfkit
from flask import Blueprint, jsonify, request, current_app
import jwt
from functools import wraps
from .utils import extract_user_id
import openai
import config

cvMaker_bp = Blueprint('cvMaker', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token.split(' ')[1], current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 403

        # If the token is valid, allow access to the protected route
        return f(*args, **kwargs)

    return decorated

@cvMaker_bp.route('/generate_pdf', methods=['POST'])
@token_required
def update_and_generate_pdf():
    data = request.json

    user_id = extract_user_id(request.headers.get('Authorization'))

    cv = CV.query.filter_by(user_id=user_id).first()
    if not cv:
        cv = CV(user_id=user_id)

    cv.first_name = data.get('firstName', cv.first_name)
    cv.last_name = data.get('lastName', cv.last_name)
    cv.email = data.get('email', cv.email)
    cv.phone = data.get('phone', cv.phone)
    cv.linkedin = data.get('linkedin', cv.linkedin)
    cv.github = data.get('github', cv.github)
    cv.description = data.get('description', cv.description)
    cv.technical_skills_languages = data.get('technicalSkills_languages', cv.technical_skills_languages)
    cv.technical_skills_frameworks = data.get('technicalSkills_frameworks', cv.technical_skills_frameworks)
    cv.technical_skills_development_tools = data.get('technicalSkills_developmentTools',
                                                     cv.technical_skills_development_tools)
    cv.soft_skills = data.get('softSkills', cv.soft_skills)

    db.session.add(cv)
    db.session.commit()

    School.query.filter_by(cv_id=cv.cv_id).delete()
    db.session.commit()
    for school in data.get('schools', []):
        school_data = {key: value for key, value in school.items() if key != 'cv_id'}
        new_school = School(cv_id=cv.cv_id, **school_data)
        db.session.add(new_school)

    WorkExperience.query.filter_by(cv_id=cv.cv_id).delete()
    db.session.commit()
    for work_experience in data.get('workExperiences', []):
        work_experience_data = {key: value for key, value in work_experience.items() if key != 'cv_id'}
        new_work_experience = WorkExperience(cv_id=cv.cv_id, **work_experience_data)
        db.session.add(new_work_experience)

    # Actualizează proiectele
    Project.query.filter_by(cv_id=cv.cv_id).delete()
    db.session.commit()
    for project in data.get('projects', []):
        project_data = {key: value for key, value in project.items() if key != 'cv_id'}
        new_project = Project(cv_id=cv.cv_id, **project_data)
        db.session.add(new_project)

    db.session.commit()

    # Generarea PDF-ului
    html_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'template.html')
    with open(html_template_path, 'r') as file:
        html_template = file.read()

    # Render the HTML template with formData
    rendered_html = render_template_string(html_template, formData=data)

    # Define the path for the temporary PDF file
    temp_dir = os.path.join(os.path.dirname(__file__), 'resumes')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    pdf_path = os.path.join(temp_dir, f'resume_{user_id}.pdf')

    # Specify the path to wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    # Configure options for pdfkit (optional)
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'enable-local-file-access': '',
    }

    # Convert the HTML to PDF using pdfkit
    pdfkit.from_string(rendered_html, pdf_path, options=options, configuration=config)

    # Save the PDF path in the CV
    cv.pdf_path = pdf_path
    db.session.commit()

    # Check if the PDF file was created
    if not os.path.exists(pdf_path):
        return jsonify({'message': 'Error: PDF file was not created.'}), 500

    return send_file(pdf_path, as_attachment=True, download_name='resume.pdf')


@cvMaker_bp.route('/get_cv/<user_id>', methods=['GET'])
@token_required
def get_cv(user_id):
    print(user_id)
    cv = CV.query.filter_by(user_id=user_id).first()
    if not cv:
        return jsonify({'message': 'CV not found'}), 404

    pdf_path = cv.pdf_path
    print (pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name='resume.pdf')


@cvMaker_bp.route('/get_cv_data', methods=['GET'])
@token_required
def get_cv_data():
    user_id = extract_user_id(request.headers.get('Authorization'))
    cv = CV.query.filter_by(user_id=user_id).first()
    if not cv:
        return jsonify({'message': 'CV not found'}), 404

    schools = [school.to_dict() for school in cv.schools]
    work_experiences = [work_experience.to_dict() for work_experience in cv.work_experiences]
    projects = [project.to_dict() for project in cv.projects]
    cv_data = cv.to_dict()

    cv_data['schools'] = schools
    cv_data['workExperiences'] = work_experiences
    cv_data['projects'] = projects

    return jsonify(cv_data)

@cvMaker_bp.route('/rephrase_text', methods=['POST'])
@token_required
def rephrase_description():
    data = request.json
    text = data.get('text')
    openai.api_key = config.OPEN_AI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that makes text sound professional and elaborate."},
            {"role": "user", "content": f"Rephrase the following text to be more professional and longer:\n\n{text}"}
        ],
        max_tokens=100,
        temperature=0.6,
    )

    rephrased_text = response.choices[0].message['content'].strip()
    return jsonify({'rephrasedText': rephrased_text})


@cvMaker_bp.route('/is_public/<user_id>', methods=['GET'])
@token_required
def is_public(user_id):
    cv = CV.query.filter_by(user_id=user_id).first()
    if not cv:
        return jsonify({'message': 'CV not found'}), 404

    return jsonify({'is_public': cv.public})


@cvMaker_bp.route('/toggle_public', methods=['POST'])
@token_required
def toggle_public():
    user_id = extract_user_id(request.headers.get('Authorization'))
    cv = CV.query.filter_by(user_id=user_id).first()
    if not cv:
        return jsonify({'message': 'CV not found'}), 404

    cv.public = not cv.public
    db.session.commit()

    return jsonify({'public': cv.public})





