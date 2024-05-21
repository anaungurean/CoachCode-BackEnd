from flask import Blueprint, request, jsonify
from app.auth import User
import jwt
from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .utils import extract_user_id
from app.database import db
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


@profileUser_bp.route('/update_profile', methods=['PUT'])
@token_required
def update_profile():
    token = request.headers.get('Authorization')
    user_id = extract_user_id(token)
    user = User.query.filter_by(id=user_id).first()
    data = request.get_json()
    
    if data.get('username') and User.query.filter_by(username=data['username']).first():
        user.username = data['username']
    else:
        return jsonify({'message': 'Username already exists'}), 400
    
    if data.get('first_name'):
        user.first_name = data['first_name']
    if data.get('last_name'):
        user.last_name = data['last_name']
    if data.get('photo_url'):
        user.photo_url = data['photo_url']
    if data.get('status'):
        user.status = data['status']
    if data.get('goal'):
        user.goal = data['goal']
    if data.get('programming_languages'):
        user.programming_languages = data['programming_languages']
    if data.get('linkedin_url'):
        user.linkedin_url = data['linkedin_url']
    if data.get('github_url'):
        user.github_url = data['github_url']
    if data.get('password'):
        user.password = data['password']
        
    db.session.commit()
    return jsonify(user), 200

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
    return jsonify(user), 200


    
     
     

    
     




    
