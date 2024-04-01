from localbin import db
from flask_login import UserMixin


# User model used to store user name and hashed password
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
    def __str__(self):
        return self.username
