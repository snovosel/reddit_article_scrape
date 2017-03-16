from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import praw

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.from_object('config')
app.secret_key = 'a1b2c3d4e5'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

reddit = praw.Reddit(client_id='G8HdzYvrHMLXgA',
                     client_secret='Y39-VftD0Q60hlZXpwJVWTioJhI',
                     redirect_uri='http://127.0.0.1:5000/',
                     user_agent='putain-quoi')


mail = Mail(app)

from reddit_article_scrape import views, models
