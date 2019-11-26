import app

from datetime import datetime
from faker import Faker
from forms.validate import CHOICES

fake = Faker()

for _, institution in CHOICES:
    for _ in range(10):
        certificate = app.Certificate(code=fake.isbn13(separator="-"),
                                      owner=fake.name(),
                                      issue_date=datetime.strptime(
                                          fake.date(pattern="%d/%m/%Y",
                                                    end_datetime=None),
            "%d/%m/%Y"), institution=institution)
        app.db.session.add(certificate)
        print("Added {}".format(certificate))
app.db.session.commit()
