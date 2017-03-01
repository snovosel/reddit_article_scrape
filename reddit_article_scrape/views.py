from flask import render_template, abort, request, flash, redirect, url_for
from reddit_article_scrape import app, db, login_manager
from reddit_article_scrape.utils import send_mail, get_info
from reddit_article_scrape.forms import RegistrationForm, LoginForm
from reddit_article_scrape.models import User
from flask_login import login_required, login_user, logout_user


@app.route('/', methods=['GET', 'POST'])
def index():
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

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    print form.errors
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        print user.username

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/subchoice')
@login_required
def subchoice():
    return render_template('subchoice.html')


@app.route('/result', methods=['POST'])
def result():
    return get_info()
