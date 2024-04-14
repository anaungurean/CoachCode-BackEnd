from .problem_model import Problem
from flask import Blueprint, jsonify, request

problem_bp = Blueprint('problems', __name__)

@problem_bp.route('/problems', methods=['GET'])
def get_all_problems():
    problems = Problem.get_all_problems()
    return jsonify(problems), 200

@problem_bp.route('/problems/<int:problem_id>', methods=['POST'])
def get_problem_by_id(problem_id):
    problem = Problem.get_problem_by_id(problem_id)
    if problem:
        return jsonify(problem), 200
    else:
        return jsonify({"error": "Problem not found"}), 404

