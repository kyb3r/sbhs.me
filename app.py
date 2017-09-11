from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
import time
app = Flask(__name__)

client_id = 'sbhs-me'
client_secret = 'YcqjZeIP1W32vKzlMjJYYn_EqrY'
auth_base_url = 'https://student.sbhs.net.au/api/authorize'
token_url = 'https://student.sbhs.net.au/api/token'
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return open('tests.html').read()

@app.route('/login')
def login():
    print('_______________BEFORE_AUTHORISATION_____________________')
    print(session)
    print('____________________________________')
    sbhs = OAuth2Session(client_id)
    authorization_url, state = sbhs.authorization_url(auth_base_url)
    session['oauth_state'] = state
    print('_______________AFTER_AUTHORISATION_____________________')
    print(session)
    print('____________________________________')
    return redirect(authorization_url)

@app.route('/callback', methods=['GET'])
def callback():
    time.sleep(1)
    print('______________Before_FETCH_TOKEN_________________')
    print(session)
    print('____________________________________')
    sbhs = OAuth2Session(client_id, state=session['oauth_state'])
    token = sbhs.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)
    session['oauth_token'] = token['access_token']
    print('______________After_FETCH_TOKEN_________________')
    print(session)
    print('____________________________________')
    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    time.sleep(1)
    print('_______________BEFORE_PROFILE_REDIRECT___________________')
    print(session)
    print('____________________________________')
    sbhs = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(sbhs.get('https://student.sbhs.net.au/api/details/userinfo.json').json())

if __name__ == '__main__':
    os.environ['DEBUG'] = "1"
    app.run(debug=True, port=os.environ.get('PORT'))


