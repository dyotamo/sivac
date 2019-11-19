import csv
import datetime
import app


def import_csv(f):
    csv_reader = csv.DictReader(f, delimiter=',')

    loaded_count = 0
    ignored_count = 0

    errors = []

    for row in csv_reader:
        certificate = app.Certificate(**row)

        if app.Certificate.query.filter_by(code=certificate.code).first() is None:
            # Put the correct issue date data
            certificate.issue_date = datetime.datetime.strptime(
                certificate.issue_date, "%d/%m/%Y").date()

            app.db.session.add(certificate)
            loaded_count += 1
        else:
            ignored_count += 1
            continue

    app.db.session.commit()
    return loaded_count, ignored_count


if __name__ == "__main__":
    print('{} line(s) processed, {} line(s) ignored'.format(
        *import_csv(open("fixture.csv"))))
