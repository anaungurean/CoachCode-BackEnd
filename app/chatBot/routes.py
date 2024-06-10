import time
from flask import Blueprint, jsonify, request, current_app
import openai
import config

chatBot_bp = Blueprint('chatBot', __name__)
openai.api_key = config.OPEN_AI_API_KEY

@chatBot_bp.route('/chatEthan', methods=['POST'])
def chat_ethan():
    data = request.json
    user_message = data.get("message")
    conversation_history = data.get("conversation_history", [])

    # Ensure the initial system message is in the conversation history
    if not conversation_history:
        conversation_history.append(
            {"role": "system", "content": 'You are Ethan, a highly skilled AI. Provide detailed feedback, identify bugs, and give actionable suggestions to improve and fix the code.'}
        )

    # Add the user's message to the conversation history
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
            "netlify", "vercel", "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack"
        ]
        return any(keyword in message.lower() for keyword in keywords)

    print(is_relevant_message_ethan(user_message))
    if not is_relevant_message_ethan(user_message):
        irrelevant_response = "I'm here to help with code reviews, bug identification, and coding improvements. Please ask a related question."
        conversation_history.append({"role": "assistant", "content": irrelevant_response})
        return jsonify({"response": irrelevant_response, "conversation_history": conversation_history})

    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=conversation_history
    )

    chat_response = response.choices[0].message['content']
    conversation_history.append({"role": "assistant", "content": chat_response})

    return jsonify({"response": chat_response, "conversation_history": conversation_history})



@chatBot_bp.route('/chatAva', methods=['POST'])
def chat_ava():
    data = request.json
    user_message = data.get("message")
    conversation_history = data.get("conversation_history", [])


    # Ensure the initial system message is in the conversation history
    if not conversation_history:
        conversation_history.append(
            {"role": "system", "content": 'You are Ava, a friendly Job Search Advisor in IT. Provide expert advice and practical tips on crafting CVs, acing interviews, and navigating job offers. Be supportive and encouraging. Answer in maximum 100 words.'}
        )

    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})

    def is_relevant_message(message):
        keywords = [
            "CV", "resume", "interview", "job offer", "job search", "cover letter", "application",
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
            "job search", "job seeker", "job candidate", "job applicant", "job seeker", "job seeker"
         ]
        return any(keyword in message.lower() for keyword in keywords)

    print (is_relevant_message(user_message))
    if not is_relevant_message(user_message):
        irrelevant_response = "I'm here to help with job search advice, including CVs, interviews, and job offers. Please ask a related question."
        conversation_history.append({"role": "assistant", "content": irrelevant_response})
        return jsonify({"response": irrelevant_response, "conversation_history": conversation_history})

    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=conversation_history,
        max_tokens=150,  # Adjust to ensure the response is concise
        temperature=0.7
    )

    chat_response = response.choices[0].message['content']
    conversation_history.append({"role": "assistant", "content": chat_response})

    return jsonify({"response": chat_response, "conversation_history": conversation_history})


@chatBot_bp.route('/generateHRQuestions', methods=['POST'])
def generateHRQuestions():
    data = request.get_json()
    job_title = data.get('jobTitle')
    number_of_questions = data.get('numberOfQuestions')

    # Ensure job_title and number_of_questions are provided
    if not job_title or not number_of_questions:
        return jsonify({"error": "Both jobTitle and numberOfQuestions are required"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a highly skilled HR interviewer. Generate {number_of_questions} HR interview questions for the role of {job_title}. These should be common HR questions, focusing on behavioral and situational aspects, rather than technical specifics. Start with easier questions like 'Tell me about yourself' and gradually move to more complex questions."
            }
        ]
    )

    generated_questions = response.choices[0].message['content'].strip('" ')

    question_list = [q.strip() for q in generated_questions.split('\n') if q.strip()]

    return jsonify({"questions": question_list})


@chatBot_bp.route('/generateFeedbackHR', methods=['POST'])
def generateFeedbackHR():
    data = request.get_json()
    interview_data = data.get('interviewData')
    print(interview_data)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are Mia, an HR professional providing feedback to a candidate. Write concise feedback for this {interview_data} . Include both positive aspects and areas for improvement. Be constructive and supportive."
            }
        ]
    )
    feedback = response.choices[0].message['content'].strip('" ')
    print(feedback)

    return jsonify({"feedback": feedback})












