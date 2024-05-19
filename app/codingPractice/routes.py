import jwt
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .problem_model import Problem

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
    return jsonify(problems), 200

@problem_bp.route('/problems/<int:problem_id>', methods=['GET'])
@token_required
def get_problem_by_id(problem_id):
    problem = Problem.get_problem_by_id(problem_id)

    if problem:
        print(problem)
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
