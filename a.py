from flask import Flask, render_template, jsonify, request
import requests
import json
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_POST=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='**********',
    MAIL_PASSWORD='**********',
    MAIL_DEFAULT_SENDER='**********',
)

mail = Mail(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods= ['POST'])
def result():
    url = request.form['sub']
    a = requests.get('https://api.reddit.com/r/' + url, headers={'User-agent': 'putain-quoi'}).json()
    children = a['data']['children']
    post_list = []

    for post in children:

        posts = {}

        posts['title'] = post['data']['title']
        posts['score'] = post['data']['score']
        posts['url'] = post['data']['url']

        post_list.append(posts)

    final = sorted(post_list, reverse=True)

    email = request.form['email']
    msg = Message(recipients=[email])
    msg.html = render_template('result.html', final=final)
    mail.send(msg)

    return render_template('result.html', final=final)



if __name__ == ('__main__'):
    app.run(debug=True)

