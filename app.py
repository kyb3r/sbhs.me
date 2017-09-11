from flask import Flask, render_template, session, redirect, url_for
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
import os

app = Flask(__name__)

client_id = 'sbhs-me'
client_secret = 'YcqjZeIP1W32vKzlMjJYYn_EqrY'
auth_base_url = 'https://student.sbhs.net.au/api/authorize'

@app.route('/')
def index():
    return open('tests.html').read()

@app.route('/login')
def login():
    sbhs = OAuth2Session(client_id)
    authorization_url, state = sbhs.authorization_url(auth_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback', methods=['GET'])
def callback():
    sbhs = OAuth2Session(client_id, state=session['oauth_state'])
    token = sbhs.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)
    session['oauth_token'] = token

    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    sbhs = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(sbhs.get('https://student.sbhs.net.au/api/details/userinfo.json').json())

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=os.environ.get('PORT'))

  
