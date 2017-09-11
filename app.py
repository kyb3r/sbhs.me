from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)


@app.route("/")
def demo():
    return '<h1>Hello this is a website!!!!! WOWOWOWOWOWO! c=====3</h1>'


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('PORT'))
