from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    
    db.init_app(app)
    
    from app.routes import admin_bp, client_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)
    
    return app