from os import environ
from smtplib import SMTP_SSL


def send_mail(msg):
    gmail_user = 'dyotamo.dev@gmail.com'
    gmail_password = environ["PASSWORD"]

    sent_from = gmail_user
    to = ['dyotamo@gmail.com', ]
    subject = 'Deu Merda no SIVAC'

    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, msg)

    server = SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
