from app.database import db
from sqlalchemy.dialects.postgresql import ARRAY

class Problem(db.Model):
    __tablename__ = 'problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    difficulty = db.Column(db.String(1000), nullable=False)
    companies = db.Column(db.String(1000), nullable=False)
    related_topics = db.Column(db.String(1000), nullable=False)
    asked_by_faang = db.Column(db.Boolean, nullable=False)
    similar_questions = db.Column(db.String(1000), nullable=False)
    tests = db.Column(db.JSON, nullable=True)
    input_variables = db.Column(db.JSON, nullable=True)
    solution = db.Column(db.JSON, nullable=True)
    hints = db.Column(ARRAY(db.String(1000)), nullable=True)
    question = db.Column(db.JSON, nullable=True)
    base_code =  db.Column(db.JSON, nullable=True)

    @classmethod
    def get_all_problems(cls):
        problems = cls.query.all()
        return [problem.to_dict() for problem in problems]

    @classmethod
    def get_problem_by_id(cls, problem_id):
        problem = cls.query.filter_by(id=problem_id).first()
        return problem.to_dict() if problem else None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty,
            "companies": self.companies,
            "related_topics": self.related_topics,
            "asked_by_faang": self.asked_by_faang,
            "similar_questions": self.similar_questions,
            "tests": self.tests,
            "input_variables": self.input_variables,
            "solution": self.solution,
            "hints": self.hints,
            "question": self.question,
            "base_code": self.base_code
        }


