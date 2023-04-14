import os
import smtplib
from email.mime.text import  MIMEText
from email.mime.multipart import MIMEMultipart

asta_gmail = os.environ["BOT_GMAIL"]
g_pass = os.environ["GMAIL_PASS"]
owner_gmail = os.environ["OWN_GMAIL"]



def sendgmail(subjek,body):
  message = MIMEMultipart()
  message["From"] = asta_gmail
  message["To"] = owner_gmail
  message["Subject"] = subjek
  message.attach(MIMEText(body, "plain"))
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(asta_gmail, g_pass)
  text = message.as_string()
  server.sendmail(asta_gmail, owner_gmail, text)
  server.quit()
  return True
