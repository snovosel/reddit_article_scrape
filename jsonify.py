from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
	data = main()
	return jsonify(data)

def main():
	return requests.get('https://api.reddit.com/r/worldnews', headers={'user-agent': 'putain-quoi'}).json()


if __name__ == "__main__":
	app.run(debug=True)
