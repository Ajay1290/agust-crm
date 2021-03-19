from flask_mail import Message
from manager.ext import mail
from flask import current_app

def send_email(to, subject, template):
    msg = Message(  subject,
                    recipients=[to],
                    html=template,
                    sender= 'noreply@agustcrm.com')
    mail.send(msg)
