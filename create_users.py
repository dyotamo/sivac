import os
import app

from werkzeug.security import generate_password_hash
from forms.search import CHOICES


for _, institution in CHOICES:
    user = app.User(institution=institution,
                    password=generate_password_hash(os.environ["PASSWORD"]))
    app.db.session.add(user)
    print("Added {}".format(user))
app.db.session.commit()
