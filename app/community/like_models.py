from app.database import db

class QuestionLike(db.Model):
    __tablename__ = 'question_likes'

    like_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.relationship('Question', backref='likes')
    user = db.relationship('User', backref='question_likes')

    def __init__(self, question_id, user_id):
        self.question_id = question_id
        self.user_id = user_id

    def __repr__(self):
        return '<QuestionLike %r>' % self.like_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class AnswerLike(db.Model):
    __tablename__ = 'answer_likes'

    like_id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.answer_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answer = db.relationship('Answer', backref='likes')
    user = db.relationship('User', backref='answer_likes')

    def __init__(self, answer_id, user_id):
        self.answer_id = answer_id
        self.user_id = user_id

    def __repr__(self):
        return '<AnswerLike %r>' % self.like_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


