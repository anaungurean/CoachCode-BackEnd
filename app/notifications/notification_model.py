from app.database import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id_to_be_notified = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id_that_triggered = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    notification_type = db.Column(db.String(10), nullable=False)
    seen = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    # Define relationships
    user_to_be_notified = db.relationship('User', foreign_keys=[user_id_to_be_notified])
    user_that_triggered = db.relationship('User', foreign_keys=[user_id_that_triggered])
    question = db.relationship('Question')


    def __init__(self, user_id_to_be_notified, user_id_that_triggered, notification_type, question_id):
        self.user_id_to_be_notified = user_id_to_be_notified
        self.user_id_that_triggered = user_id_that_triggered
        self.notification_type = notification_type
        self.question_id = question_id

    def __repr__(self):
        return '<Notification %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'user_id_to_be_notified': self.user_id_to_be_notified,
            'user_id_that_triggered': self.user_id_that_triggered,
            'question_id': self.question_id,
            'notification_type': self.notification_type,
            'seen': self.seen,
            'created_at': self.created_at
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()