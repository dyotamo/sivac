from datetime import datetime
from os.path import join
from csv import DictReader
from tempfile import gettempdir
from werkzeug.utils import secure_filename
from models import db, Certificate

def save_csv(form):
    """ An utility function to save a file in the /tmp directory,
    returning its path for further processing """
    csv = form.csv.data
    path = join(gettempdir(), secure_filename(csv.filename))
    csv.save(path)
    return path


def import_csv(f):
    csv_reader = DictReader(f, delimiter=',')

    for row in csv_reader:
        certificate = Certificate(**row)
        if Certificate.query.filter_by(code=certificate.code).first() is None:
            certificate.issue_date = datetime.strptime(
                certificate.issue_date, "%d/%m/%Y").date()
            db.session.add(certificate)
    db.session.commit()