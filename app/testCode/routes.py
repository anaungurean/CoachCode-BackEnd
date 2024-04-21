import requests

from .code_model import Code
from flask import Blueprint, jsonify, request
from .utilis import test_code

code_bp = Blueprint('testCode', __name__)

@code_bp.route('/test', methods=['GET'])
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

    print(expected_output)
    print(type(expected_output))



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


JDoodle_clientId = 'bafef15d11484bd3888d2ddb9bb439e7'
JDoodle_clientSecret = 'ceed32d3c74566bd40a87eb20495e15a554b529ba18a10db15dc29b04e153077'

@code_bp.route('/executeCode', methods=['POST'])
def execute_code():
    # Extract the code, language, and input from the request's JSON body
    content = request.json
    print(content)
    code = content['script']
    language = content['language']
    stdin = content['stdin']

    # Prepare the data for the JDoodle API request
    data = {
        'clientId': JDoodle_clientId,
        'clientSecret': JDoodle_clientSecret,
        'script': code,
        'language': language,
        'versionIndex': '0',
        'stdin': stdin
    }

    # Make a POST request to the JDoodle API
    response = requests.post('https://api.jdoodle.com/v1/execute', json=data)

    # Return the response from JDoodle API to the client
    return jsonify(response.json())
