from flask import render_template, abort
from reddit_article_scrape import app
from reddit_article_scrape.utils import send_mail, get_info


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    return get_info()
