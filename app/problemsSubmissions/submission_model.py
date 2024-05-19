from flask import jsonify

from app.database import db

class Submission(db.Model):
    __tablename__ = 'problems_submissions'

    submission_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    programming_language = db.Column(db.String(1000), nullable=False)
    submission = db.Column(db.String(1000), nullable=False)
    memory = db.Column(db.Integer, nullable=False)
    runtime = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    @classmethod
    def get_all_submissions(cls):
        return cls.query.all()

    @classmethod
    def get_submission_by_id(cls, submission_id):
        return cls.query.filter_by(submission_id=submission_id).first()

    @classmethod
    def get_submissions_by_problem_id(cls, problem_id):
        return cls.query.filter_by(problem_id=problem_id).all()

    @classmethod
    def get_submissions_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


    @classmethod
    def get_submissions_by_user_id_and_problem_id_and_programming_language(cls, user_id, problem_id, programming_language):
        return cls.query.filter_by(user_id=user_id, problem_id=problem_id, programming_language=programming_language).first()

    def save_submission(self):
        if self.get_submissions_by_user_id_and_problem_id_and_programming_language(self.user_id, self.problem_id, self.programming_language):
             delete_submission = self.get_submissions_by_user_id_and_problem_id_and_programming_language(self.user_id, self.problem_id, self.programming_language)
             db.session.delete(delete_submission)
        db.session.add(self)
        db.session.commit()

    def delete_submission(self):
        db.session.delete(self)
        db.session.commit()


    def to_dict(self):
        return {
            'submission_id': self.submission_id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'programming_language': self.programming_language,
            'submission': self.submission,
            'memory': self.memory,
            'runtime': self.runtime,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }