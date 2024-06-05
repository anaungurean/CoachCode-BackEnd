from app.database import db

class WorkExperience(db.Model):
    __tablename__ = 'work_experiences'

    work_experience_id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.cv_id'), nullable=False)
    position = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    startDate = db.Column(db.Text)
    endDate = db.Column(db.Text)
    responsibilities = db.Column(db.Text)

    def to_dict(self):
        return {
            'work_experience_id': self.work_experience_id,
            'cv_id': self.cv_id,
            'position': self.position,
            'company': self.company,
            'location': self.location,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'responsibilities': self.responsibilities
        }

