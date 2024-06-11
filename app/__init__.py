from flask import Flask
from flask_cors import CORS
from .database import db
from .auth.routes import auth_bp
from .codingPractice.routes import problem_bp
from .problemsSubmissions.routes import submission_bp
from .profileUser.routes import profileUser_bp
from .community.routes import community_bp
from  .cvMaker.routes import cvMaker_bp
from .notifications.routes import notifications_bp
from .chatBot.routes import chatBot_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(profileUser_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(cvMaker_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(chatBot_bp)

    CORS(app)

    return app
