import csv
import datetime
import app


def import_csv(f):
    csv_reader = csv.DictReader(f, delimiter=',')
    line_count = 0
    for row in csv_reader:
        certificate = app.Certificate(**row)
        certificate.issue_date = datetime.datetime.strptime(
            certificate.issue_date, "%d/%m/%Y").date()
        app.db.session.add(certificate)
        line_count += 1
    app.db.session.commit()
    f.close()
    return line_count


if __name__ == "__main__":
    print(print(f'Processed {import_csv(open("fixture.csv"))} lines.'))
