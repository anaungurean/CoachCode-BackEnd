import jwt
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .question_model import Question
from .answer_model import Answer
from .like_models import QuestionLike, AnswerLike
from .utils import extract_user_id
from flask import send_file
from ..auth import User
import os
from werkzeug.utils import secure_filename

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

        return f(*args, **kwargs)

    return decorated


@community_bp.route('/questions', methods=['GET'])
@token_required
def get_all_questions():
    questions = Question.query.order_by(Question.posting_date.desc()).all()
    output = []
    for question in questions:
        user_id = question.user_id
        user = User.query.get(user_id)
        question_data = {
            'id': question.question_id,
            'title': question.title,
            'content': question.content,
            'posting_date': question.posting_date,
            'user_id': question.user_id,
            'topic': question.topic,
            'photo': question.photo,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        output.append(question_data)
    return jsonify(output)


@community_bp.route('/questions_photo/<int:question_id>', methods=['GET'])
def get_question_photo(question_id):
    question = Question.query.get_or_404(question_id)
    if not question.photo:
        return jsonify({'message': 'This question does not have a photo'}), 404
    return send_file(question.photo, mimetype='image/jpeg')




@community_bp.route('/questions', methods=['POST'])
@token_required
def post_question():
    title = request.form.get('title')
    content = request.form.get('content')
    topic = request.form.get('topic')
    file = request.files.get('photo')
    save_path = None

    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400

    if file:
        filename = secure_filename(f'question_{title}.png')
        save_path = os.path.join('C:\\Users\\anama\\OneDrive\\Desktop\\BackEnd\\app\\community\\PhotoQuestion', filename)
        file.save(save_path)

    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
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
    title = request.form.get('title')
    content = request.form.get('content')
    topic = request.form.get('topic')
    file = request.files.get('photo')
    save_path = None

    if file:
        filename = secure_filename(f'question_{title}.png')
        save_path = os.path.join('C:\\Users\\anama\\OneDrive\\Desktop\\BackEnd\\app\\community\\PhotoQuestion', filename)
        file.save(save_path)

    question = Question.query.get_or_404(question_id)
    question.title = title
    question.content = content
    question.topic = topic
    question.photo = save_path
    question.save()
    return jsonify({'message': 'Question updated successfully'}), 200



@community_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@token_required
def delete_question(question_id):
    likes = QuestionLike.query.filter_by(question_id=question_id).all()
    for like in likes:
        like.delete()
    answers = Answer.query.filter_by(question_id=question_id).all()
    for ans in answers:
        ans.delete()
    question = Question.query.get_or_404(question_id)
    question.delete()
    return jsonify({'message': 'Question deleted successfully'}), 200

@community_bp.route('/questions/<int:question_id>/answers', methods=['POST'])
@token_required
def post_answer(question_id):
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    question = Question.query.get_or_404(question_id)
    content = request.json.get('content')
    new_answer = Answer(content=content, user_id=user_id, question_id=question_id)
    new_answer.save()
    return jsonify({'message': 'Answer posted successfully'}), 201



@community_bp.route('/questions/<int:question_id>/answers', methods=['GET'])
@token_required
def get_answers(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    output = []
    for answer in answers:
        user = User.query.get(answer.user_id)
        answer_data = {
            'id': answer.answer_id,
            'content': answer.content,
            'posting_date': answer.posting_date,
            'user_id': answer.user_id,
            'question_id': answer.question_id,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        output.append(answer_data)
    return jsonify(output)

@community_bp.route('/questions/<int:question_id>/like', methods=['POST'])
@token_required
def like_question(question_id):
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    existing_like = QuestionLike.query.filter_by(question_id=question_id, user_id=user_id).first()
    if existing_like:
        return jsonify({'message': 'You have already liked this question'}), 400

    new_like = QuestionLike(question_id=question_id, user_id=user_id)
    new_like.save()
    return jsonify({'message': 'Question liked successfully'}), 201

@community_bp.route('/questions/<int:question_id>/like', methods=['DELETE'])
@token_required
def unlike_question(question_id):
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    existing_like = QuestionLike.query.filter_by(question_id=question_id, user_id=user_id).first()
    if not existing_like:
        return jsonify({'message': 'You have not liked this question yet'}), 400

    existing_like.delete()
    return jsonify({'message': 'Question unliked successfully'}), 200


@community_bp.route('/questions/<int:question_id>/is_liked', methods=['GET'])
@token_required
def is_question_liked(question_id):
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    existing_like = QuestionLike.query.filter_by(question_id=question_id, user_id=user_id).first()
    if existing_like:
        return jsonify(True)
    return jsonify(False)



@community_bp.route('/questions/<int:question_id>/likes', methods=['GET'])
@token_required
def get_question_likes(question_id):
    likes = QuestionLike.query.filter_by(question_id=question_id).all()
    return jsonify(len(likes))


@community_bp.route('/answers/<int:answer_id>' , methods=['DELETE'])
@token_required
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    answer.delete()
    return jsonify({'message': 'Answer deleted successfully'}), 200





