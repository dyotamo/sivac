import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
from sivac import application
from forms.validate import CHOICES
from models import db, User

with application.app_context():
    for _, institution in CHOICES:
        user = User(institution=institution, password=generate_password_hash(os.environ["PASSWORD"]))
        db.session.add(user)
    db.session.commit()
