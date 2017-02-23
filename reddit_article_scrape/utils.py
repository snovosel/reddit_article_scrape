from flask import render_template
from flask_mail import Message
from reddit_article_scrape import mail


def send_mail(email, message):
    msg = Message(recipients=[email])
    msg.html = render_template('result.html', final=message)
    mail.send(msg)
