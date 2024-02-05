import requests
import sys
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

with open(sys.argv[1], "r") as f:
    cr = json.load(f)

def manda_telegram():
    message = f"{sys.argv[2]}: {sys.argv[3]}"
    url = f"https://api.telegram.org/bot{cr['telegram']['token_id']}/sendMessage?chat_id={cr['telegram']['chat_id']}&text={message}"
    requests.get(url).json()

def manda_mail():
    message = MIMEMultipart("alternative")
    message["Subject"] = sys.argv[2]
    message["From"] = cr["mail"]["sender_email"]
    message["To"] = cr["mail"]["reciever_email"]

    text = sys.argv[3]
    html = f"<html><body><p>{sys.argv[3]}</p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP(cr["mail"]["smtp_server"], cr["mail"]["port"]) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(cr["mail"]["sender_email"], cr["mail"]["password"])
        server.sendmail(cr["mail"]["sender_email"], cr["mail"]["reciever_email"], message.as_string())


if len(sys.argv) > 4:
    if sys.argv[4] == "mail":
        manda_mail()
    elif sys.argv[4] == "telegram":
        manda_telegram()
else:
    manda_mail()
    manda_telegram()
