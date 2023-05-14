import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(smtp_server, port, send_from, send_to, subject, text=None, password=None):
    mime = MIMEMultipart("alternative")
    mime["Subject"] = subject
    mime["From"] = send_from
    mime["To"] = send_to
    if text:
        mime.attach(MIMEText(text, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        if password:
            server.starttls(context=context)
            server.login(send_from, password)
        server.sendmail(send_from, send_to, mime.as_string())
