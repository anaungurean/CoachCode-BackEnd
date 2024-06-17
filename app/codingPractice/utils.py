from app.problemsSubmissions import Submission
from flask import jsonify, current_app, request
import jwt
import config
from openai import OpenAI
import openai

openai.api_key = config.OPEN_AI_API_KEY
client = OpenAI(api_key=config.OPEN_AI_API_KEY)

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


def generate_hints(problem_description):

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages =[
        {
            "role": "system",
            "content": ("You are a helpful assistant. Enumerate three short hints for the following problem: " + problem_description+
                        "I want to follow the format: 1. Hint 1\n2. Hint 2\n3. Hint 3\n"
                        )

        }
        ]
    )

    response = response.choices[0].message.content.strip()
    hints = [hint.strip() for hint in response.split("\n") if hint.strip() != ""]
    return hints

def generate_solutions(problem_description):

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages =[
        {
            "role": "system",
            "content": ("You are a helpful assistant. Provide a solution in Python for the following problem. Make sure to structure your solution in a class 'Solution' with necessary methods. "
                        "Include the main method to read from keyboard and print the result without other additional messages. Give me only the code, don't include explanation.  " + problem_description )
        }]
      )

    solution_python = response.choices[0].message.content.strip()
    solution_python = solution_python.replace("```", "")
    solution_python = solution_python.replace("python", "")

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages =[
        {
            "role": "system",
            "content": ("You are a helpful assistant. Provide a solution in Java for the following problem. Make sure to structure your solution in a class 'Solution' with necessary methods. "
                        "Include the main method to read from keyboard and print the result without other additional messages. Give me only the code, don't include explanation.  " + problem_description )
        }]
      )

    solution_java = response.choices[0].message.content.strip()
    solution_java = solution_java.replace("```", "")
    solution_java = solution_java.replace("java", "")

    json = {
        "python": solution_python,
        "java": solution_java
    }

    return json




def generate_question(problem_description):
    prompt = (
        f"You are a helpful assistant. Based on the following problem description, generate a short theoretical question "
        f"with multiple-choice options and identify the correct answer. The response should have the following structure:\n"
        f"{{\n"
        f"  \"question\": \"Your question here\",\n"
        f"  \"options\": {{\n"
        f"    \"A\": \"Option A\",\n"
        f"    \"B\": \"Option B\",\n"
        f"    \"C\": \"Option C\",\n"
        f"    \"D\": \"Option D\",\n"
        f"    \"E\": \"Option E\"\n"
        f"  }},\n"
        f"  \"correct_answer\": \"Correct option letter\"\n"
        f"}}\n"
        f"Problem description: {problem_description}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract the generated content
    generated_question = response.choices[0].message.content.strip()
    generated_question = generated_question.replace("\n", "")
    generated_question = generated_question.replace("\"", " ")
    print(generated_question)


    return generated_question

















