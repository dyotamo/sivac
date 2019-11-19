import app

from random import randint
from datetime import datetime
from faker import Faker

fake = Faker()

INSTITUTIONS = ["Universidade Zambeze"]

for institution in INSTITUTIONS:
    for _ in range(10):
        certificate = app.Certificate(code=fake.isbn13(separator="-"), owner=fake.name(), issue_date=datetime.strptime(
            fake.date(pattern="%d/%m/%Y", end_datetime=None), "%d/%m/%Y"), institution=institution)
        app.db.session.add(certificate)

        print("Added {}".format(certificate))
    app.db.session.commit()

print("Done")
