import smtplib, ssl
import os
from _socket import gaierror
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = os.environ['SMTP_PORT']
SERVER = os.environ['SMTP_SERVER']
SENDER = os.environ['SENDER']
RECEIVER = os.environ['RECEIVER']
PASSWORD = os.environ['SMTP_PASSWORD']


def connect_to_smtp_server(data):
    message = MIMEMultipart("alternative")
    message["Subject"] = data.get('subject')
    message["From"] = data.get('user_mail')
    message["To"] = RECEIVER
    part1 = MIMEText(data.get('message'), "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    status_code = _send_email(context, message)
    return status_code


def _send_email(context, message):
    try:
        with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, message.as_string())
            print('Sent')
            return 200
    except (gaierror, ConnectionRefusedError):
        print('Failed to connect to the server. Bad connection settings?')
        return 400
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
        return 400
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))
        return 500

