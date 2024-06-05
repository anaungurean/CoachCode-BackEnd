from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.auth import User
import jwt
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .utils import extract_user_id
from app.database import db
from flask import send_file
import os

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

profileUser_bp = Blueprint('profile_user', __name__)

@profileUser_bp.route('/my_profile', methods=['GET'])
@token_required
def my_profile():
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    print(user_id)
    user = User.query.filter_by(id=user_id).first()
    print(user.to_dict())
    return jsonify(user.to_dict()), 200


@profileUser_bp.route('/update_general_information', methods=['PUT'])
@token_required
def update_profile():
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    user = User.query.filter_by(id=user_id).first()
    data = request.get_json()

    if data.get('username') and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    else:
        user.username = data['username']
    
    if data.get('first_name'):
        user.first_name = data['first_name']
    if data.get('last_name'):
        user.last_name = data['last_name']
    if data.get('status'):
        user.status = data['status']
    if data.get('goal'):
        user.goal = data['goal']

    db.session.commit()
    return jsonify({'message': 'Profile updated'}), 200

@profileUser_bp.route('/delete_profile', methods=['DELETE'])
@token_required
def delete_profile():
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

@profileUser_bp.route('/all_users', methods=['GET'])
@token_required
def all_users():
    users = User.query.all()
    return jsonify(users), 200

@profileUser_bp.route('/user/<int:user_id>', methods=['GET'])
@token_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.to_dict()), 200


@profileUser_bp.route('/user_photo/<int:user_id>', methods=['GET'])
def user_photo(user_id):
    user = User.query.get_or_404(user_id)
    photo_path = user.get_photo_url()
    if not photo_path:
        photo_path = 'C:\\Users\\anama\\OneDrive\\Desktop\\BackEnd\\app\\profileUser\\PhotoUser\\default_user_photo.jpg'
    return send_file(photo_path, mimetype='image/jpeg')


@profileUser_bp.route('/upload_photo', methods=['POST'])
@token_required
def upload_photo():
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    user = User.query.filter_by(id=user_id).first()
    file = request.files['file']

    if user.photo_url:
        os.remove(user.photo_url)

    filename = f'{user_id}_user_photo.jpg'
    save_path = os.path.join('C:\\Users\\anama\\OneDrive\\Desktop\\BackEnd\\app\\profileUser\\PhotoUser', filename)
    file.save(save_path)

    user.photo_url = save_path
    db.session.commit()

    return jsonify({'message': 'Photo uploaded'}), 200

@profileUser_bp.route('/update_social_accounts', methods=['PUT'])
@token_required
def update_social_accounts():
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    user = User.query.filter_by(id=user_id).first()
    data = request.get_json()

    if data.get('linkedin_url'):
        user.linkedin_url = data['linkedin_url']
    if data.get('github_url'):
        user.github_url = data['github_url']
    if data.get('facebook_url'):
        user.facebook_url = data['facebook_url']

    db.session.commit()
    return jsonify({'message': 'Social accounts updated'}), 200


@profileUser_bp.route('/update_password', methods=['PUT'])
@token_required
def update_password():
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    user = User.query.filter_by(id=user_id).first()
    data = request.get_json()

    if not user.verify_password(data['current_password']):
        return jsonify({'message': 'Invalid password'}), 400


    user.update_password(data['new_password'])
    return jsonify({'message': 'Password updated'}), 200



