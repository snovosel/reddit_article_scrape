from flask import render_template, request
import requests
from flask_mail import Message
from reddit_article_scrape import mail


def send_mail(email, message):
    msg = Message(recipients=[email])
    msg.html = render_template('result.html', final=message)
    mail.send(msg)


def get_info():
    url = request.form.get('sub')
    email = request.form.get('email')
    if not url:
        abort(404)
    a = requests.get('https://api.reddit.com/r/' + url, headers={'User-agent': 'putain-quoi'}).json()
    children = a.get('data', {}).get('children')
    if not children:
        return "There was an error", 502

    post_list = [ { key: post['data'][key] for key in post['data'] if key in ('title', 'url', 'score') } for post in children]

    final = sorted(post_list, key=lambda k: k['score'], reverse=True)

    try:
        send_mail(email, final)
    except Exception:
        print("Sending mail as failed")


    return render_template('result.html', final=final)
