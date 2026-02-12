"""
Minimal Flask app to serve the budget tracker web UI locally.
Run: python server.py  (or: flask --app server run)
Then open http://127.0.0.1:5000 in your browser.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
