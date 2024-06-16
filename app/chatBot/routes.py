import time
from flask import Blueprint, jsonify, request, current_app
import openai
import config
from openai import OpenAI
import uuid
import traceback
import jwt
from functools import wraps

chatBot_bp = Blueprint('chatBot', __name__)
openai.api_key = config.OPEN_AI_API_KEY
client = OpenAI(api_key=config.OPEN_AI_API_KEY)
ASSISTANT_ID = config.ASSISTANT_ID

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

        return f(*args, **kwargs)

    return decorated


@chatBot_bp.route('/chatEthan', methods=['POST'])
@token_required
def chat_ethan():
    data = request.json
    user_message = data.get("message")
    conversation_history = data.get("conversation_history", [])

    if not conversation_history:
        conversation_history.append(
            {"role": "system", "content": 'You are Ethan, a highly skilled AI. Provide detailed feedback, identify bugs, and give actionable suggestions to improve and fix the code.'}
        )

    conversation_history.append({"role": "user", "content": user_message})

    def is_relevant_message_ethan(message):
        keywords = [
            "bug", "debug", "error", "exception", "crash", "failure", "issue", "problem",
            "code review", "feedback", "optimize", "optimization", "performance", "refactor",
            "clean code", "coding standards", "best practices", "code quality", "improve code",
            "fix code", "code improvement", "code suggestions", "code feedback", "syntax error",
            "logical error", "runtime error", "compile error", "unit test", "integration test",
            "testing", "test case", "function", "method", "class", "module", "library",
            "API", "framework", "algorithm", "data structure", "code style", "naming convention",
            "code formatting", "linting", "static analysis", "dynamic analysis", "profiling",
            "code efficiency", "complexity", "code readability", "maintainability", "software design",
            "design pattern", "coding issue", "development", "programming", "implementation", "solution",
            "algorithmic problem", "algorithmic challenge", "algorithmic task", "algorithmic exercise",
            "algorithmic question", "algorithmic test", "algorithmic practice", "algorithmic coding",
            "algorithmic competition", "algorithmic contest", "algorithmic site", "algorithmic platform",
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin", "typescript",
            "go", "rust", "scala", "r", "perl", "bash", "shell", "sql", "html", "css", "xml", "json",
            "yaml", "markdown", "docker", "kubernetes", "aws", "azure", "gcp", "firebase", "heroku",
            "netlify", "vercel", "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack", "c",
            "programming language", "web development", "mobile development", "cloud computing", "devops",
            "software engineering", "software development", "software architecture", "software testing",
            "software deployment", "software maintenance", "software support", "software documentation",
            "software versioning", "software licensing", "software security", "software compliance",
            "bug tracking", "issue tracking", "version control", "continuous integration", "continuous deployment",
            "hello", "hi", "hey", "howdy", "greetings", "good morning", "good afternoon", "good evening",
            "good night", "good day", "goodbye", "farewell", "see you", "talk to you", "chat with you",
            "help", "support", "assist", "aid", "guide", "advise", "recommend", "suggest", "propose",
            "explain", "clarify", "elaborate", "detail", "describe", "define", "specify", "identify",
            "recognize", "diagnose", "analyze", "evaluate", "assess", "review", "inspect", "examine",
            "test", "verify", "validate", "check", "audit", "audit", "audit", "audit", "audit", "audit",
            "thank", "thanks", "appreciate", "grateful", "gratitude", "thankful", "thank you", "thanks a lot",

        ]
        return any(keyword in message.lower() for keyword in keywords)

    if not is_relevant_message_ethan(user_message):
        irrelevant_response = "I'm here to help with code reviews, bug identification, and coding improvements. Please ask a related question."
        conversation_history.append({"role": "assistant", "content": irrelevant_response})
        return jsonify({"response": irrelevant_response, "conversation_history": conversation_history})

    response = client.chat.completions.create(
        model='gpt-4',
        messages=conversation_history
    )

    chat_response = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": chat_response})

    return jsonify({"response": chat_response, "conversation_history": conversation_history})



@chatBot_bp.route('/chatAva', methods=['POST'])
@token_required
def chat_ava():
    data = request.json
    user_message = data.get("message")
    conversation_history = data.get("conversation_history", [])

    if not conversation_history:
        conversation_history.append(
            {"role": "system", "content": 'You are Ava, a friendly Job Search Advisor in IT. Provide expert advice and practical tips on crafting CVs, acing interviews, and navigating job offers. Be supportive and encouraging. Answer in maximum 100 words.'}
        )

    conversation_history.append({"role": "user", "content": user_message})

    def is_relevant_message(message):
        keywords = [
            "cv", "resume", "interview", "job offer", "job search", "cover letter", "application",
            "networking", "salary negotiation", "job opening", "career advice", "hiring process",
            "LinkedIn", "portfolio", "references", "job market", "employment", "job position",
            "recruitment", "headhunter", "job board", "job fair", "internship", "freelance",
            "contract", "full-time", "part-time", "career transition", "job description",
            "job posting", "application status", "background check", "skills", "qualifications",
            "professional development", "career growth", "mentorship", "career path", "promotion",
            "network", "cover letter", "soft skills", "hard skills", "career change", "job opportunities",
            "industry trends", "work experience", "resume tips", "interview tips", "job tips",
            "career coaching", "job applications", "resume writing", "job hunting", "job strategies",
            "career goals", "job leads", "interview preparation", "job advice", "workplace advice",
            "job success", "career success", "interview questions", "job interviews", "career planning",
            "employment opportunities", "career management", "job strategy", "employment tips",
            "career tips", "work tips", "job search tips", "employment advice", "career advice",
            "resume advice", "job search strategy", "interview strategy", "job market trends",
            "career opportunities", "networking events", "job fairs", "career fairs", "job",
            "career", "work", "employment", "job application", "job interview", "job offer",
            "job search", "job seeker", "job candidate", "job applicant", "job seeker", "job seeker",
            "help", "support", "assist", "aid", "guide", "advise", "recommend", "suggest", "propose",
            "explain", "clarify", "elaborate", "detail", "describe", "define", "specify", "identify",
            "hello", "hi", "hey", "howdy", "greetings", "good morning", "good afternoon", "good evening",
            "good night", "good day", "goodbye", "farewell", "see you", "talk to you", "chat with you",
            "thank", "thanks", "appreciate", "grateful", "gratitude", "thankful", "thank you", "thanks a lot",

         ]
        return any(keyword in message.lower() for keyword in keywords)

    if not is_relevant_message(user_message):
        irrelevant_response = "I'm here to help with career advice, including CVs, interviews, and job hints. Please ask a related question."
        conversation_history.append({"role": "assistant", "content": irrelevant_response})
        return jsonify({"response": irrelevant_response, "conversation_history": conversation_history})

    response = client.chat.completions.create(
        model='gpt-4',
        messages=conversation_history,
        max_tokens=150,
        temperature=0.7
    )

    chat_response = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": chat_response})

    return jsonify({"response": chat_response, "conversation_history": conversation_history})


@chatBot_bp.route('/generateHRQuestions', methods=['POST'])
@token_required
def generateHRQuestions():
    data = request.get_json()
    job_title = data.get('jobTitle')
    number_of_questions = data.get('numberOfQuestions')

    if not job_title or not number_of_questions:
        return jsonify({"error": "Both jobTitle and numberOfQuestions are required"}), 400

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a highly skilled HR interviewer. Generate {number_of_questions} HR interview questions for the role of {job_title}. These should be common HR questions, focusing on behavioral and situational aspects, rather than technical specifics. Start with easier questions like 'Tell me about yourself' and gradually move to more complex questions."
            }
        ]
    )

    generated_questions = response.choices[0].message.content.strip()
    question_list = [q.strip() for q in generated_questions.split('\n') if q.strip()]

    return jsonify({"questions": question_list})


@chatBot_bp.route('/generateFeedbackHR', methods=['POST'])
@token_required
def generateFeedbackHR():
    data = request.get_json()
    interview_data = data.get('interviewData')
    print(interview_data)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Mia, an HR professional providing feedback to the candidate. For each interview question, provide structured feedback "
                    "with the following format:\n\n"
                    "Question: [The interview question]\n"
                    "Answer: [The candidate's response]\n"
                    "\tplus: [Positive aspects of the answer]\n"
                    "\tminus: [Areas for improvement]\n\n"
                    "Be constructive and supportive in your feedback. Here is the interview data:\n\n"
                    f"{interview_data}"
                )
            }
        ]
    )

    feedback = response.choices[0].message.content.strip()
    return jsonify({"feedback": feedback})


@chatBot_bp.route('/generateTechnicalQuestions', methods=['POST'])
@token_required
def generateTechnicalQuestions():
    data = request.get_json()
    job_title = data.get('jobTitle')
    number_of_questions = data.get('numberOfQuestions')

    if not job_title or not number_of_questions:
        return jsonify({"error": "Both jobTitle and numberOfQuestions are required"}), 400

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a highly skilled Technical  interviewer. Generate {number_of_questions} Technical  interview questions for the role of {job_title}. These should be common technical questions, focus on technical specifics."
            }
        ]
    )

    generated_questions = response.choices[0].message.content.strip()
    question_list = [q.strip() for q in generated_questions.split('\n') if q.strip()]
    return jsonify({"questions": question_list})


@chatBot_bp.route('/generateFeedbackTechnical', methods=['POST'])
@token_required
def generateFeedbackTechnical():
    data = request.get_json()
    interview_data = data.get('interviewData')

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Lucas, an HR professional providing feedback to the candidate. For each interview question, provide structured feedback "
                    "with the following format:\n\n"
                    "Question: [The interview question]\n"
                    "Answer: [The candidate's response]\n"
                    "\tplus: [Positive aspects of the answer]\n"
                    "\tminus: [Areas for improvement]\n\n"
                    "Be constructive and supportive in your feedback. Here is the interview data:\n\n"
                    f"{interview_data}"
                )
            }
        ]
    )

    feedback = response.choices[0].message.content.strip()
    return jsonify({"feedback": feedback})

threads = {}

def get_assistant_id(client):
    try:
        response = client.beta.assistants.list()
        assistants = response.data
        for assistant in assistants:
            if assistant.name == 'Ana':
                return assistant.id
        return None
    except Exception as e:
        print("An error occurred while fetching the assistant ID:", str(e))
        print(traceback.format_exc())
        return None


@chatBot_bp.route('/chatAna', methods=['POST'])
@token_required
def ask_assistant():
    data = request.get_json()

    user_id = data.get("user_id")
    user_message = data.get("message")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if user_id in threads:
        thread_id = threads[user_id]
        print("Thread ID exists")
    else:
        thread_id = str(uuid.uuid4())
        threads[user_id] = thread_id

    try:
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ]
        )


        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id='asst_dbuFX2cr8nRT0rUFeTMq1epx')

        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(1)

        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data
        latest_message = messages[0]

        return jsonify({"response": latest_message.content[0].text.value})

    except Exception as e:
        print("An error occurred:", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500










