#!/usr/bin/env python3
"""The App Module"""
import flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', method='GET', strict_slashes=False)
def Home():
    """Home page
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
