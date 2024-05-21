from app.problemsSubmissions import Submission
from flask import jsonify, current_app, request
import jwt

def check_submission_exists(user_id, problem_id):
    """
    Check if a submission for a given user_id and problem_id exists.
    """
    submission = Submission.get_submissions_by_user_id_and_problem_id(user_id, problem_id)
    return submission is not None

def extract_user_id(token):
    try:
        data = jwt.decode(token.split(' ')[1], current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 403