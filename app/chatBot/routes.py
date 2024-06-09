import time
from flask import Blueprint, jsonify, request, current_app
import openai
import config

chatBot_bp = Blueprint('chatBot', __name__)
openai.api_key = config.OPEN_AI_API_KEY

@chatBot_bp.route('/chatEthan', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    conversation_history = data.get("conversation_history", [])

    # Ensure the initial system message is in the conversation history
    if not conversation_history:
        conversation_history.append(
            {"role": "system", "content": 'You are a highly skilled AI. Provide detailed feedback, identify bugs, and give actionable suggestions to improve and fix the code.'}
        )

    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})
    print(conversation_history)

    # Generate a response from OpenAI
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=conversation_history
    )

    # Extract and format the response
    chat_response = response.choices[0].message['content']

    # Add the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": chat_response})

    # Return the response and updated conversation history as JSON
    return jsonify({"response": chat_response, "conversation_history": conversation_history})
