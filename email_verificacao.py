import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase


def email_verificacao():

    smtp_server = "smtp.gmail.com"

    port = 587  # For starttls
    sender_email = "healthberry1@gmail.com"
    receiver_email = "cjvborges@yahoo.com"
    password = "healthberry111&"
    subject = "Hello"
    # Create the plain-text and HTML version of your message
    message = """\
        Subject: Hello World


        Hi there!

        This message is sent from Python."""

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
