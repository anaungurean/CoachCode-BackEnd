from .code_model import Code
from flask import Blueprint, jsonify, request
from .utilis import test_code

code_bp = Blueprint('testCode', __name__)

@code_bp.route('/test', methods=['POST'])
def test():
    data = request.get_json()

    if 'language' not in data or 'code' not in data or 'input' not in data:
        return jsonify({"error": "Cerere JSON invalidă: language, code și input sunt necesare"}), 400

    language = data['language']
    code = data['code']
    input_data = data['input']
    expected_output = data['expected_output']
    expected_output = expected_output.replace('[', '(')
    expected_output = expected_output.replace(']', ')')

    try:
        output, error = test_code(language, code, input_data)
        print(output, error)
        output = output.replace('\n', '')
        print(output, expected_output)
        print(type (output), type (expected_output))
        if expected_output == output:
            return jsonify({"output": output, "error": error, "result": "passed"})
        else:
            return jsonify({"output": output, "error": error, "result": "failed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
