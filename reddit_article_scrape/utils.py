from flask import render_template, abort, request, flash, redirect, url_for
import requests
from flask_mail import Message
from reddit_article_scrape import mail, db, reddit
from reddit_article_scrape.forms import LoginForm, RegistrationForm
from reddit_article_scrape.models import User, Favorite
from flask_login import login_required, login_user, logout_user, current_user


def send_mail(email, message):
    return True
    msg = Message(recipients=[email])
    msg.html = render_template('result.html', data=message)
    mail.send(msg)

def get_info(subreddit):
    return reddit.subreddit(subreddit).hot(limit=10)

def serialize_post(post):
    return dict(title=post.title, score=post.score, id=post.id, url=post.url)

def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            return render_template('invalid_login.html')

        elif user.is_correct_password(form.password.data):
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

        try:
            db.session.add(user)
            db.session.commit()
            print user.username
            return redirect(url_for('index'))

        except:
            return render_template('duplicate.html')

    return render_template('register.html', form=form)
