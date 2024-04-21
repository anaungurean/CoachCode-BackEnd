from .problem_model import Problem
from flask import Blueprint, jsonify, request

problem_bp = Blueprint('problems', __name__)

@problem_bp.route('/problems', methods=['GET'])
def get_all_problems():
    problems = Problem.get_all_problems()
    return jsonify(problems), 200

@problem_bp.route('/problems/<int:problem_id>', methods=['GET'])
def get_problem_by_id(problem_id):
    problem = Problem.get_problem_by_id(problem_id)

    if problem:
        print(problem)
        return jsonify(problem), 200
    else:
        return jsonify({"error": "Problem not found"}), 404

@problem_bp.route('/problems/<string:title>', methods=['GET'])
def get_id_by_title(title):
    problem = Problem.query.filter_by(title=title).first()
    if problem:
        return jsonify(problem.id), 200
    else:
        return jsonify({"error": "Problem not found"}), 404

