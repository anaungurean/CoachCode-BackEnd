import jwt
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .submission_model import Submission
import datetime
from .utils import extract_user_id, get_title_of_problem_by_id
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

submission_bp = Blueprint('submissions', __name__)

@submission_bp.route('/submissions', methods=['GET'])
@token_required
def get_all_submissions():
    submissions = Submission.get_all_submissions()
    return jsonify(submissions), 200

@submission_bp.route('/submissions/<int:submission_id>', methods=['GET'])
@token_required
def get_submission_by_id(submission_id):
    submission = Submission.get_submission_by_id(submission_id)

    if submission:
        return jsonify(submission), 200
    else:
        return jsonify({"error": "Submission not found"}), 404

@submission_bp.route('/submissions/<int:problem_id>', methods=['GET'])
@token_required
def get_submissions_by_problem_id(problem_id):
    submissions = Submission.get_submissions_by_problem_id(problem_id)
    return jsonify(submissions), 200

@submission_bp.route('/submissions_user/<int:user_id>', methods=['GET'])
@token_required
def get_submissions_by_user_id(user_id):
    """
    Get all submissions for a given user ID.
    This route is protected by token authentication.
    """
    try:
        # Fetch submissions for the specified user_id
        submissions = Submission.get_submissions_by_user_id(user_id)
        if submissions is None:
            return jsonify({"message": "No submissions found for this user."}), 404

        # Convert submissions to a JSON serializable format if necessary
        submissions_list = [submission.to_dict() for submission in submissions]

        for submission in submissions_list:
            submission['problem_title'] = get_title_of_problem_by_id(submission['problem_id'])

        print(submissions_list)
        return jsonify(submissions_list), 200
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500


@submission_bp.route('/submissions', methods=['POST'])
@token_required
def save_submission():
    data = request.get_json()
    submission = Submission(
        user_id=extract_user_id(request.headers.get('Authorization')),
        problem_id=data['problem_id'],
        programming_language=data['programming_language'],
        submission=data['submission'],
        memory=data['memory'],
        runtime=data['runtime'],
        timestamp= datetime.datetime.now()
    )
    submission.save_submission()
    return jsonify(submission.to_dict()), 201


@submission_bp.route('/submissions/<int:submission_id>', methods=['DELETE'])
@token_required
def delete_submission(submission_id):
    submission = Submission.get_submission_by_id(submission_id)

    if submission:
        submission.delete_submission()
        return jsonify({"message": "Submission deleted"}), 200
    else:
        return jsonify({"error": "Submission not found"}), 404





