from flask import jsonify

from app.database import db

class School(db.Model):
    __tablename__ = 'schools'

    school_id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.cv_id'), nullable=False)
    school = db.Column(db.String(100))
    degree = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    city = db.Column(db.String(50))

    def to_dict(self):
        return {
            'school_id': self.school_id,
            'cv_id': self.cv_id,
            'school': self.school,
            'degree': self.degree,
            'graduation_year': self.graduation_year,
            'city': self.city
        }

    @classmethod
    def get_all_schools(cls):
        return cls.query.all()

    @classmethod
    def get_school_by_id(cls, school_id):
        return cls.query.filter_by(school_id=school_id).first()