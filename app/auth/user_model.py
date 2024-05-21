from app.database import db
from passlib.hash import bcrypt_sha256

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    photo_url = db.Column(db.String(255))
    status = db.Column(db.String(100))
    goal = db.Column(db.Text)
    programming_languages = db.Column(db.ARRAY(db.String))
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_user(cls, email, password, first_name=None, last_name=None, username=None, programming_languages=None, photo_url=None, status=None, goal=None, linkedin_url=None, github_url=None):
        hashed_password = bcrypt_sha256.hash(password)
        new_user = cls(first_name=first_name, last_name=last_name, email=email, password=hashed_password, username=username, programming_languages=programming_languages, photo_url=photo_url, status=status, goal=goal, linkedin_url=linkedin_url, github_url=github_url)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update_password(self, new_password):
        self.password = bcrypt_sha256.hash(new_password)
        db.session.commit()

    def verify_password(self, password):
        return bcrypt_sha256.verify(password, self.password)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'photo_url': self.photo_url,
            'status': self.status,
            'goal': self.goal,
            'programming_languages': self.programming_languages,
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url
        }
