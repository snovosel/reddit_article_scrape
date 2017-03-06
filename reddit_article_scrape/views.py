from flask import render_template, redirect, url_for, abort, request
from reddit_article_scrape import app, db
from reddit_article_scrape.utils import send_mail, get_info, login, create_user, show_posts
from reddit_article_scrape.models import User, Favorite
from flask_login import login_required, logout_user, current_user


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

@app.route('/favorites')
@login_required
def favorites():
    favorite = Favorite.query.get(current_user.id)
    if favorite == None:
        return render_template('none_found.html')
    return render_template('favorites.html', favorite=favorite)

@app.route('/result', methods=['POST'])
def result():
    return show_posts()

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_to_favorites/<post>', methods=['GET', 'POST'])
def add_to_favorites(post):
    data = get_info()
    post = data[post]
    fav= Favorite(title=data.get('title'), url=data.get('url'), score=data.get('score'), user_id=current_user.id)
    db.session.add(fav)
    db.session.commit()
