#!/usr/bin/env python3
"""The App Module"""
from flask import Flask, jsonify, request, abort, url_for, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def Home():
    """Home page
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Register new users
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not password and not email:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)

        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Log out user and return to the home page
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect(url_for('Home'))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
