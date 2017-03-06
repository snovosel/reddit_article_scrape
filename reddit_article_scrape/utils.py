from flask import render_template, abort, request, flash, redirect, url_for
import requests
from flask_mail import Message
from reddit_article_scrape import mail, db
from reddit_article_scrape.forms import LoginForm, RegistrationForm
from reddit_article_scrape.models import User, Favorite
from flask_login import login_required, login_user, logout_user, current_user


def send_mail(email, message):
    msg = Message(recipients=[email])
    msg.html = render_template('result.html', data=message)
    mail.send(msg)

def get_info():
    url = request.form.get('sub')
    if not url:
        abort(404)
    a = requests.get('https://api.reddit.com/r/' + url, headers={'User-agent': 'putain-quoi'}).json()
    children = a.get('data', {}).get('children')
    if not children:
        return "There was an error", 502

    post_list = [ { key: post['data'][key] for key in post['data'] if key in ('title', 'url', 'score') } for post in children]
    final = sorted(post_list, key=lambda k: k['score'], reverse=True)

    return final

def show_posts():
    data = get_info()
    email = request.form.get('email')

    try:
        send_mail(email, data)
    except Exception:
        print("Sending mail as failed")

    return render_template('result.html', data=data)

def save_post(data):
    data = request.form.get('post')
    #post = data[post]
    fav= Favorite(title=data.get('title'), url=data.get('url'), score=data.get('score'), user_id=current_user.id)
    db.session.add(fav)
    db.session.commit()


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
