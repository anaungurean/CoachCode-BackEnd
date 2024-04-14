from app.database import db
from passlib.hash import bcrypt_sha256

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_user(cls, email, password):
        hashed_password = bcrypt_sha256.hash(password)
        new_user = cls(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update_password(self, new_password):
        self.password = bcrypt_sha256.hash(new_password)
        db.session.commit()

    def verify_password(self, password):
        return bcrypt_sha256.verify(password, self.password)
