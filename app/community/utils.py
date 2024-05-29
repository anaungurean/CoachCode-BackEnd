from flask import jsonify, current_app, request
import jwt

def extract_user_id(token):
    try:
        data = jwt.decode(token.split(' ')[1], current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 403