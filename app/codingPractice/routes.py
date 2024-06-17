import jwt
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .problem_model import Problem
from .utils import  check_submission_exists, extract_user_id, generate_hints, generate_solutions, generate_question, generate_tests

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

        # Dacă tokenul este valid, permite accesul la ruta protejată
        return f(*args, **kwargs)

    return decorated

problem_bp = Blueprint('problems', __name__)

@problem_bp.route('/problems', methods=['GET'])
@token_required
def get_all_problems():
    problems = Problem.get_all_problems()
    user_id = extract_user_id(request.headers.get('Authorization'))
    for problem in problems:
        is_solved = check_submission_exists(user_id, problem['id'])
        problem['is_solved'] = is_solved

    return jsonify(problems), 200

@problem_bp.route('/problems/<int:problem_id>', methods=['GET'])
@token_required
def get_problem_by_id(problem_id):
    problem = Problem.get_problem_by_id(problem_id)
    user_id = extract_user_id(request.headers.get('Authorization'))
    is_solved = check_submission_exists(user_id, problem_id)

    if problem['hints'] is None:
        new_hints = generate_hints(problem['description'])
        Problem.add_hints(problem['id'], new_hints)
        problem['hints'] = new_hints

    if problem['solution'] is None:
        solutions = generate_solutions(problem['description'])
        Problem.add_solution(problem['id'], solutions)
        problem['solution'] = solutions
    problem['is_solved'] = is_solved

    if problem['question'] is None:
        question = generate_question(problem['description'])
        Problem.add_question(problem['id'], question)
        problem['question'] = question

    if problem['tests'] is  None:
        tests = generate_tests(problem['description'])
        Problem.add_tests(problem['id'], tests)
        problem['tests'] = tests

    if problem:
        return jsonify(problem), 200
    else:
        return jsonify({"error": "Problem not found"}), 404

@problem_bp.route('/problems/<string:title>', methods=['GET'])
@token_required
def get_id_by_title(title):
    problem = Problem.query.filter_by(title=title).first()
    if problem:
        return jsonify(problem.id), 200
    else:
        return jsonify({"error": "Problem not found"}), 404


@problem_bp.route('/problems/title/<int:problem_id>', methods=['GET'])
@token_required
def get_title_of_problem_by_id(problem_id):
    problem = Problem.query.filter_by(id=problem_id).first()
    if problem:
        return jsonify(problem.title), 200
    else:
        return jsonify({"error": "Problem not found"}), 404
