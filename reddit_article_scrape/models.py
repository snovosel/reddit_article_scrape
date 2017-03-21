from reddit_article_scrape import db, bcrypt, login_manager
from flask_login import UserMixin, current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password= db.Column(db.String(128))
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_correct_password(self, password):
        if bcrypt.check_password_hash(self.password, password):
            return True

    def __repr__(self):
        return '<User %r>' % (self.email)


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    url = db.Column(db.String())
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return dict(id= self.id, title= self.title, url= self.url, score= self.score)

    @classmethod
    def from_submission(cls, submission):
        return cls(title=submission.title, url=submission.url, score=submission.score, user_id=current_user.id)
