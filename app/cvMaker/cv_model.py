from flask import jsonify

from app.database import db


class CV(db.Model):
    __tablename__ = 'cv'

    cv_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    description = db.Column(db.Text)
    technical_skills_languages = db.Column(db.Text)
    technical_skills_frameworks = db.Column(db.Text)
    technical_skills_development_tools = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    pdf_path = db.Column(db.String(255))
    public = db.Column(db.Boolean, default=False)

    schools = db.relationship('School', backref='cv', cascade="all, delete-orphan")
    work_experiences = db.relationship('WorkExperience', backref='cv', cascade="all, delete-orphan")
    projects = db.relationship('Project', backref='cv', cascade="all, delete-orphan")


    @classmethod
    def get_all_cvs(cls):
        return cls.query.all()

    @classmethod
    def get_cv_by_id(cls, cv_id):
        return cls.query.filter_by(cv_id=cv_id).first()

    @classmethod
    def get_cv_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save_cv(self):
        db.session.add(self)
        db.session.commit()

    def delete_cv(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'cv_id': self.cv_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'linkedin': self.linkedin,
            'github': self.github,
            'description': self.description,
            'technical_skills_languages': self.technical_skills_languages,
            'technical_skills_frameworks': self.technical_skills_frameworks,
            'technical_skills_development_tools': self.technical_skills_development_tools,
            'soft_skills': self.soft_skills,
            'pdf_path': self.pdf_path
        }