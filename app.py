from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template, g
from flask.json import jsonify
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'jyuukverixxsupascretkeywtflmao'

client_id = 'sbhs-me'
client_secret = 'YcqjZeIP1W32vKzlMjJYYn_EqrY'
auth_base_url = 'https://student.sbhs.net.au/api/authorize'
token_url = 'https://student.sbhs.net.au/api/token'
auth_required_endpoints = (
    'barcodenews/list.json',
    'dailynews/list.json',
    'diarycalendar/events.json',
    'details/particiaption.json',
    'details/userinfo.json',
    'timetable/daytimetable.json',
    'timetable/timetable.json',
    )

def login_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get('logged_in'):
              return render_template('template.html', 
                top='Unauthorized!', 
                bot='You need to be logged in for that.'
                )
            else:
              return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/')
def index():
    '''Home page, still need to work on it.'''
    if session.get('logged_in') is None:
        session['logged_in'] = False 
    return render_template('countdown.html', logged_in=1 if session['logged_in'] else 0)

@app.route('/login')
def login():
    '''Redirects to oauth'''
    sbhs = OAuth2Session(client_id)
    authorization_url, state = sbhs.authorization_url(auth_base_url)
    session['oauth_state'] = state 
    return redirect(authorization_url)

@app.route('/logged-in')
def _logged_in():
    return render_template('template.html', top='Logged In!', bot='sbhs.me')

@app.route('/logout')
def logout():
    '''Clears the session and logs out.'''
    if session.get('logged_in'):
        session.clear()
        return render_template('template.html', top='Logged Out!', bot='sbhs.me')
    else:
        return render_template('template.html', top='You cant log out!', bot='If you are not logged in!')

@app.route('/callback', methods=['GET'])
def callback():
    '''The url that is the user is redirected to'''
    sbhs = OAuth2Session(client_id, state=session['oauth_state'])
    token = sbhs.fetch_token(token_url, 
                             client_secret=client_secret,
                             authorization_response=request.url)
    session['oauth_token'] = token
    session['logged_in'] = True
    return redirect(url_for('_logged_in'))

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

@app.route('/api/<path:endpoint>', methods=["GET"])
@login_required()
def dynamic(endpoint):
    if endpoint not in auth_required_endpoints:
        return '<h1>Invalid Endpoint!</h1>\n' \
               '<p>Auth endpoints:\n{}</p>' \
               .format(', '.join(auth_required_endpoints))

    sbhs = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(sbhs.get(f'https://student.sbhs.net.au/api/{endpoint}').json())


if __name__ == '__main__':
    os.environ['DEBUG'] = "1"
    app.run(debug=True, port=os.environ.get('PORT'))

