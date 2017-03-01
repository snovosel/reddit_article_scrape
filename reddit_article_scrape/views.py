from flask import render_template, redirect, url_for
from reddit_article_scrape import app, db
from reddit_article_scrape.utils import send_mail, get_info, login, create_user
from flask_login import login_required, logout_user


@app.route('/', methods=['GET', 'POST'])
def index():
    return login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return create_user()

@app.route('/subchoice')
@login_required
def subchoice():
    return render_template('subchoice.html')


@app.route('/result', methods=['POST'])
def result():
    return get_info()

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))
