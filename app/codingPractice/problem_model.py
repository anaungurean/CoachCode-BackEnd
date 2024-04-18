from app.database import db

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
            "similar_questions": self.similar_questions
        }
