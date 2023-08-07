from werkzeug.security import check_password_hash

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    fullname = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(102), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    profile_picture = db.Column(db.LargeBinary)

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
