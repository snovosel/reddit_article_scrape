from flask import render_template, abort, request, flash, redirect, url_for
import requests
from flask_mail import Message
from reddit_article_scrape import mail, db
from reddit_article_scrape.forms import LoginForm, RegistrationForm
from reddit_article_scrape.models import User
from flask_login import login_required, login_user, logout_user



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



def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            return redirect(url_for('subchoice'))

        else:
            print "incorrect pass"
            return redirect(url_for('index'))

    return render_template('index.html', form=form)

def create_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        print user.username
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
