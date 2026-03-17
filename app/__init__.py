from flask import Flask
from flask_cors import CORS
from config import Config
from app.models.db import init_db
from app.routes.jobs import jobs_bp
from app.routes.resumes import resumes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    init_db()
    app.register_blueprint(jobs_bp, url_prefix='/api')
    app.register_blueprint(resumes_bp, url_prefix='/api')
    return app
