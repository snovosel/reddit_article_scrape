from flask import render_template, redirect, url_for, abort, request, jsonify, json
from reddit_article_scrape import app, db, reddit
from reddit_article_scrape.utils import send_mail, get_info, login, create_user, serialize_post
from reddit_article_scrape.models import User, Favorite
from flask_login import login_required, logout_user, current_user
import pdb


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

@app.route('/favs')
@login_required
def favs():
    return render_template('favorites.html')

@app.route('/favorites')
@login_required
def favorites():
    return jsonify( [ favorite.to_dict() for favorite in current_user.favorites.all() ] )

@app.route('/favorites/', methods=['DELETE'])
@login_required
def delete_favorite():
    parameters = request.get_json()
    fav_id = parameters.get('favorite')
    if fav_id:
        f = Favorite.query.get_or_404(fav_id)
        db.session.delete(f)
        db.session.commit()
        return '', 201

@app.route('/rpost', methods=['GET'])
def get_rpost():
    subreddit = request.args.get('q')
    if subreddit:
        data = get_info(subreddit)
        final = jsonify( [ serialize_post(post) for post in data ] )
        return final

@app.route('/favorite', methods=['POST'])
def add_favorite():
    parameters = request.get_json(force=True)

    post_id = parameters.get('post_id')
    if post_id:
        submission = reddit.submission(id=post_id)

        favorite = Favorite.from_submission(submission)
        db.session.add(favorite)
        db.session.commit()
        return '', 201

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))
