from flask import Blueprint, jsonify, request, current_app
from .user_model import User
from .reset_code_model import ResetCode
from .utils import generate_reset_code, send_email, bcrypt_sha256, datetime
import jwt
import datetime

auth_bp = Blueprint('users', __name__)


@auth_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = User.find_by_email(email)

    if existing_user:
        return jsonify({"error": "Email already exists"}), 409  # Conflict

    new_user = User.create_user(email, password, first_name, last_name)

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def authenticate_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.find_by_email(email)

    if not user:
        return jsonify({"error": "There is no account with this email !"}), 404
    else:
        if user.verify_password(password):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, current_app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({"message": "Authentication successful", "token": token}), 200
        else:
            return jsonify({"error": "The password is incorrect"}), 401


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.find_by_email(email)

    if user:
        reset_code = generate_reset_code()
        email_subject = "Password Reset Code"
        email_body = (f"Hello,\n\nWe received a request to reset your password. Your password reset code is: {reset_code}\n\nPlease use this code to reset your password. It is available for 15 minutes only." "\n\nIf you did not request a password reset, please ignore this email.\n\nThank you,\nCoachCode Team")
        send_email(email, email_subject, email_body)

        reset_code = ResetCode.create_reset_code(email, reset_code)
        return jsonify({"message": "Reset code sent successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@auth_bp.route('/check-resetcode', methods=['POST'])
def check_reset_code():
    data = request.json
    email = data.get('email')
    reset_code = data.get('reset_code')

    if not email or not reset_code:
        return jsonify({"error": "Email and reset code are required"}), 400

    reset_code_obj = ResetCode.find_by_email(email)
    print(reset_code_obj.reset_code, reset_code, reset_code_obj.check_if_valid())

    if reset_code_obj and reset_code_obj.reset_code == reset_code and reset_code_obj.check_if_valid():
        return jsonify({"message": "Reset code is valid"}), 200
    elif reset_code_obj and reset_code_obj.reset_code == reset_code and not reset_code_obj.check_if_valid():
        return jsonify({"error": "Reset code has expired"}), 404
    else:
        return jsonify({"error": "Invalid reset code"}), 465


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({"error": "Email and new password are required"}), 400

    user = User.find_by_email(email)
    reset_code_obj = ResetCode.find_by_email(email)

    if user:
        user.update_password(new_password)
        reset_code_obj.mark_as_used()
        return jsonify({"message": "Password reset successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

