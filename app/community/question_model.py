from app.database import db

class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    posting_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic = db.Column(db.String(100))
    photo = db.Column(db.String(1000))
    user = db.relationship('User', backref='questions')

    def __init__(self, title, content, user_id, topic, photo):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.topic = topic
        self.photo = photo

    def __repr__(self):
        return '<Question %r>' % self.title

    def serialize(self):
        return {
            'question_id': self.question_id,
            'title': self.title,
            'content': self.content,
            'posting_date': self.posting_date,
            'user_id': self.user_id,
            'topic': self.topic,
            'photo': self.photo
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
