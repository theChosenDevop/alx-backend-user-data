#!/usr/bin/env python3
import flask import Flask
import flask

app = Flask(__name__)


@app.route('/', method='GET', strict_slashes=False)
def Home():
    """Home page
    """
    return flask.jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
