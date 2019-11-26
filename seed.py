import csv
import datetime
import app


def import_csv(f):
    csv_reader = csv.DictReader(f, delimiter=',')

    for row in csv_reader:
        certificate = app.Certificate(**row)
        if app.Certificate.query.filter_by(code=certificate.code).first() is None:
            certificate.issue_date = datetime.datetime.strptime(
                certificate.issue_date, "%d/%m/%Y").date()
            app.db.session.add(certificate)
    app.db.session.commit()


if __name__ == "__main__":
    import_csv(open("./data/fixture.csv"))
