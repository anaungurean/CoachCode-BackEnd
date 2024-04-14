from app.database import db
from datetime import datetime

class ResetCode(db.Model):
    __tablename__ = 'reset_codes'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    reset_code = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    used = db.Column(db.Boolean, default=False)

    @classmethod
    def create_reset_code(cls, email, reset_code):
        existing_reset_code = cls.query.filter_by(email=email).first()

        if existing_reset_code:
            existing_reset_code.reset_code = reset_code
            existing_reset_code.created_at = datetime.now()
            existing_reset_code.used = False
            db.session.commit()
            return existing_reset_code
        else:
            new_reset_code = cls(email=email, reset_code=reset_code)
            db.session.add(new_reset_code)
            db.session.commit()
            return new_reset_code

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_reset_code(cls, reset_code):
        return cls.query.filter_by(reset_code=reset_code).first()

    def check_if_valid(self):
        if not self.used:
            reset_code_time = self.created_at
            current_time = datetime.now()
            time_difference = current_time - reset_code_time

            if time_difference.total_seconds() < 900:
                return True
            else:
                print("Reset code has expired")
                return False
        else:
            return False

    def mark_as_used(self):
        self.used = True
        db.session.commit()

