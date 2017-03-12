small python program that requests reddit json data, parses, and returns to browser as well as sends you an email.

The program also includes the links of each article, internal or external.


TO SET UP DATABASE:

in python interpreter:

  1. from reddit_article_scrape import db
  2. db.create_all()

TO SET FLASK APP VARIABLE:

  1. export FLASK_APP=reddit_article_scrape
