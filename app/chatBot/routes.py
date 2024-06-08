from flask import Blueprint, jsonify, request, current_app
import openai
import config

chatBot_bp = Blueprint('chatBot', __name__)
openai.api_key = config.OPEN_AI_API_KEY


@chatBot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    print(user_message)

    # response = openai.ChatCompletion.create(
    #     model='gpt-4',
    #     messages=[
    #         {"role": "system",
    #          "content": 'You are a highly skilled AI, answer the questions given within a maximum of 100 characters.'},
    #         {"role": "user", "content": user_message}
    #     ]
    # )

    # chat_response = response.choices[0].message['content']
    chat_response = 'Hello I am a chatbot. I am here to help you.'
    print(chat_response)
    return jsonify(chat_response)
