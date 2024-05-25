from app.database import db

class Answer(db.Model):
    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    posting_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.relationship('Question', backref='answers')
    user = db.relationship('User', backref='answers')


    def __init__(self, question_id, content, user_id):
        self.question_id = question_id
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return '<Answer %r>' % self.content

    def serialize(self):
        return {
            'answer_id': self.answer_id,
            'question_id': self.question_id,
            'content': self.content,
            'posting_date': self.posting_date,
            'user_id': self.user_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
