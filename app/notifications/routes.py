from flask import Blueprint, jsonify, request, current_app
import jwt
from functools import wraps
from app.notifications.notification_model import Notification
from app import db
from app.auth import User

notifications_bp = Blueprint('notifications', __name__)
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


@notifications_bp.route('/notifications', methods=['POST'])
@token_required
def post_notification():
    data = request.get_json()
    notification = Notification(
        user_id_that_triggered=data.get('user_id_that_triggered_notification'),
        user_id_to_be_notified=data.get('user_id_to_be_notified'),
        question_id=data.get('question_id'),
        notification_type=data.get('notification_type')
    )


    db.session.add(notification)
    db.session.commit()
    return jsonify({'message': 'Notification created successfully'}), 201


@notifications_bp.route('/notifications/<int:user_id>', methods=['GET'])
@token_required
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id_to_be_notified=user_id, seen=False).all()
    output = []
    for notification in notifications:
        user = User.query.get(notification.user_id_that_triggered)
        user_name = user.first_name + ' ' + user.last_name
        notification_data = {
            'id': notification.id,
            'user_name_that_triggered': user_name,
            'question_id': notification.question_id,
            'notification_type': notification.notification_type,
            'created_at': notification.created_at
        }
        output.append(notification_data)
    return output, 200


@notifications_bp.route('/seen_notification/<int:question_id>/<int:notification_id>', methods=['PUT'])
@token_required
def seen_notification(question_id, notification_id):
    notifications = Notification.query.filter_by(question_id=question_id, id=notification_id).all()
    for notification in notifications:
        notification.seen = True
    db.session.commit()
    return jsonify({'message': 'Notification seen'}), 200










