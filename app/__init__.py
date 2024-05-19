from flask import Flask
from flask_cors import CORS
from .database import db
from .auth.routes import auth_bp
from .codingPractice.routes import problem_bp
from .problemsSubmissions.routes import submission_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(submission_bp)

    CORS(app)

    return app
