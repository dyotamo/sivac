from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class Certificate(db.Model):
    """ Certificate model """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    owner = db.Column(db.String(120), unique=False, nullable=False)
    issue_date = db.Column(db.DateTime(), unique=False, nullable=False)
    institution = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<Certificate %s>" % self.code


class User(db.Model, UserMixin):
    """ User model """
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return "<Institution %s>" % self.institution

if __name__ == "__main__":
    from sivac import application
    with application.app_context():
        db.create_all()