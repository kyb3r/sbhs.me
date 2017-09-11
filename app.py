from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/")
def index():
    return open('tests.html').read()


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('PORT'))
