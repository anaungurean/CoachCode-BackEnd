import jwt
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .question_model import Question
from .answer_model import Answer
from .like_models import QuestionLike, AnswerLike
from .utils import extract_user_id
from flask import send_file
import os

community_bp = Blueprint('community', __name__)


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

        # Dacă tokenul este valid, permite accesul la ruta protejată
        return f(*args, **kwargs)

    return decorated


@community_bp.route('/questions', methods=['GET'])
@token_required
def get_all_questions():
    questions = Question.query.all()
    output = []
    for question in questions:
        question_data = {
            'id': question.question_id,
            'title': question.title,
            'content': question.content,
            'posting_date': question.posting_date,
            'user_id': question.user_id,
            'topic': question.topic,
            'photo': question.photo
        }
        output.append(question_data)
    return jsonify({'questions': output})


@community_bp.route('/questions', methods=['POST'])
@token_required
def post_question():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    topic = data.get('topic')
    file = request.files.get('photo')

    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400

    if file:
        filename = f'question_{title}.png'
        save_path = os.path.join('C:\\Users\\anama\\OneDrive\\Desktop\\BackEnd\\app\\community\\PhotoQuestion', filename)
        file.save(save_path)

    user_id = extract_user_id(request)
    new_question = Question(title=title, content=content, topic=topic, photo=save_path, user_id=user_id)
    new_question.save()


    return jsonify({'message': 'Question posted successfully'}), 201

@community_bp.route('/questions/<int:question_id>', methods=['GET'])
@token_required
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    return jsonify({
        'id': question.question_id,
        'title': question.title,
        'content': question.content,
        'posting_date': question.posting_date,
        'user_id': question.user_id,
        'topic': question.topic,
        'photo': question.photo
    })


@community_bp.route('/questions/<int:question_id>', methods=['PUT'])
@token_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.json
    question.title = data.get('title', question.title)
    question.content = data.get('content', question.content)
    question.topic = data.get('topic', question.topic)
    question.photo = data.get('photo', question.photo)
    question.save()
    return jsonify({'message': 'Question updated successfully'})


@community_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@token_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.user_id != extract_user_id(request):
        return jsonify({'message': 'You are not authorized to delete this question'}), 403

    question.delete()
    return jsonify({'message': 'Question deleted successfully'}), 200

@community_bp.route('/questions/<int:question_id>/answers', methods=['POST'])
@token_required
def post_answer(question_id):
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'message': 'Content is required for the answer'}), 400

    user_id = extract_user_id(request)
    new_answer = Answer(question_id=question_id, content=content, user_id=user_id)
    new_answer.save()
    return jsonify({'message': 'Answer posted successfully'}), 201

@community_bp.route('/questions/<int:question_id>/answers', methods=['GET'])
@token_required
def get_answers(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    output = []
    for answer in answers:
        answer_data = {
            'id': answer.answer_id,
            'content': answer.content,
            'posting_date': answer.posting_date,
            'user_id': answer.user_id,
            'question_id': answer.question_id
        }
        output.append(answer_data)
    return jsonify({'answers': output})


@community_bp.route('/questions/<int:question_id>/answers/<int:answer_id>', methods=['GET'])
@token_required
def get_answer(question_id, answer_id):
    answer = Answer.query.get_or_404(answer_id)
    return jsonify({
        'id': answer.answer_id,
        'content': answer.content,
        'posting_date': answer.posting_date,
        'user_id': answer.user_id,
        'question_id': answer.question_id
    })

@community_bp.route('/questions/<int:question_id>/like', methods=['POST'])
@token_required
def like_question(question_id):
    user_id = extract_user_id(request)
    existing_like = QuestionLike.query.filter_by(question_id=question_id, user_id=user_id).first()
    if existing_like:
        return jsonify({'message': 'You have already liked this question'}), 400

    new_like = QuestionLike(question_id=question_id, user_id=user_id)
    new_like.save()
    return jsonify({'message': 'Question liked successfully'}), 201

@community_bp.route('/questions/<int:question_id>/like', methods=['DELETE'])
@token_required
def unlike_question(question_id):
    user_id = extract_user_id(request)
    existing_like = QuestionLike.query.filter_by(question_id=question_id, user_id=user_id).first()
    if not existing_like:
        return jsonify({'message': 'You have not liked this question yet'}), 400

    existing_like.delete()
    return jsonify({'message': 'Question unliked successfully'}), 200


@community_bp.route('/questions/search', methods=['GET'])
@token_required
def search_questions():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({'message': 'Topic parameter is required for search'}), 400

    questions = Question.query.filter_by(topic=topic).all()
    output = []
    for question in questions:
        question_data = {
            'id': question.question_id,
            'title': question.title,
            'content': question.content,
            'posting_date': question.posting_date,
            'user_id': question.user_id,
            'topic': question.topic,
            'photo': question.photo
        }
        output.append(question_data)

    return jsonify({'questions': output})


@community_bp.route('/questions/<int:question_id>/likes', methods=['GET'])
@token_required
def get_question_likes(question_id):
    likes = QuestionLike.query.filter_by(question_id=question_id).all()
    output = []
    for like in likes:
        like_data = {
            'id': like.like_id,
            'question_id': like.question_id,
            'user_id': like.user_id
        }
        output.append(like_data)
    return jsonify({'likes': output})



