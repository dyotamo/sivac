import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from faker import Faker
from sivac import application
from forms.validate import CHOICES
from models import db, Certificate

fake = Faker()

with application.app_context():
    for _, institution in CHOICES:
        for _ in range(10):
            certificate = Certificate(code=fake.isbn13(separator="-"),
                                      owner=fake.name(),
                                      issue_date=datetime.strptime(
                                          fake.date(pattern="%d/%m/%Y",
                                                    end_datetime=None),
                "%d/%m/%Y"), institution=institution)
            db.session.add(certificate)
    db.session.commit()
