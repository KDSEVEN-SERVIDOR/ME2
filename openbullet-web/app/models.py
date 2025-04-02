from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

class Client(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID
    token = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)