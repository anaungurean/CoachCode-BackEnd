from app.database import db

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.cv_id'), nullable=False)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)
    link = db.Column(db.String(200))

    def to_dict(self):
        return {
            'project_id': self.project_id,
            'cv_id': self.cv_id,
            'name': self.name,
            'description': self.description,
            'technologies': self.technologies,
            'link': self.link
        }

