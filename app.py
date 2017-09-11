from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
import os
import time
from functools import wraps
app = Flask(__name__)

client_id = 'sbhs-me'
client_secret = 'YcqjZeIP1W32vKzlMjJYYn_EqrY'
auth_base_url = 'https://student.sbhs.net.au/api/authorize'
token_url = 'https://student.sbhs.net.au/api/token'
app.secret_key = 'blalalalababfafalfa'

def login_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session['logged_in'] is False:
              return redirect(url_for('login'))
            else:
              return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/')
def index():
    if session.get('logged_in') is None:
        session['logged_in'] = False 
    return render_template('tests.html')

@app.route('/login')
def login():
    sbhs = OAuth2Session(client_id)
    authorization_url, state = sbhs.authorization_url(auth_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/logout')
def logout():
    if session['logged_in'] is True:
        session.clear()
    return redirect(url_for('index'))

@app.route('/callback', methods=['GET'])
def callback():
    sbhs = OAuth2Session(client_id, state=session['oauth_state'])
    token = sbhs.fetch_token(token_url, 
                             client_secret=client_secret,
                             authorization_response=request.url)
    session['oauth_token'] = token
    session['logged_in'] = True
    return redirect(url_for('profile'))

@app.route("/profile", methods=["GET"])
@login_required()
def profile():
    sbhs = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(sbhs.get('https://student.sbhs.net.au/api/details/userinfo.json').json())

@app.route('/notices', methods=["GET"])
@login_required()
def daily_notices():
    sbhs = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(sbhs.get('https://student.sbhs.net.au/api/dailynews/list.json').json())


if __name__ == '__main__':
    os.environ['DEBUG'] = "1"
    app.run(debug=True, port=os.environ.get('PORT'))


