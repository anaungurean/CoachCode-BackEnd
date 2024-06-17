from app.problemsSubmissions import Submission
from flask import jsonify, current_app, request
import jwt
import config
from openai import OpenAI
import openai
import json
import re

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

def remove_hidden_characters(s):
    """
    Elimină caracterele ascunse dintr-un șir de caractere.
    """
    return re.sub(r'[\u0000-\u001F\u007F-\u009F]', '', s).strip()


def generate_question(problem_description):

    structure = {
        "question": "Your question here",
        "options": {
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D",
            "E": "Option E"
        },
        "correct_answer": "Correct option letter"
    }

    prompt = (
        f"You are a helpful assistant. Based on the following problem description, generate a short theoretical question "
        f"with multiple-choice options and identify the correct answer. The response should have the following structure, "
        f"{json.dumps(structure)} Problem description: {problem_description}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )

    question_data = json.loads(response.choices[0].message.content.strip())
    question_data['question'] = remove_hidden_characters(question_data['question'])
    question_data['correct_answer'] = remove_hidden_characters(question_data['correct_answer'])
    question_data['options'] = {k: remove_hidden_characters(v) for k, v in question_data['options'].items()}

    print(question_data)

    return question_data


def generate_tests(problem_description):
    # Construiește promptul conform structurii cerute
    prompt = (
        f"You are a helpful assistant. Generate 10 test cases for the following problem. {problem_description}\n"
        f"I want to follow this structure. Input to be one string, delimit the variables from input by slash n (/n) \n"
        f"[\n"
        f"  {{\n"
        f'    "input": "1 2 3 4 5\\n9",\n'
        f'    "output_java": "output_java_here",\n'
        f'    "output_python": "output_python_here"\n'
        f"  }},\n"
        f"]"
    )

    # Trimite promptul către API-ul OpenAI pentru a genera răspunsul
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )

    # Extrage răspunsul generat și parsează-l în teste individuale
    generated_tests =  json.loads(response.choices[0].message.content.strip())



    return  generated_tests
















