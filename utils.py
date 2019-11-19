import os
import smtplib


def send_mail(msg):
    gmail_user = 'dyotamo.dev@gmail.com'
    gmail_password = os.environ["PASSWORD"]

    sent_from = gmail_user
    to = ['dyotamo@gmail.com', ]
    subject = 'OMG Super Important Message'

    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, msg)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
