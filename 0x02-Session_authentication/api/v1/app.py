#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_inst = getenv("AUTH_TYPE")
if auth_inst:
    if auth_inst == "auth":
        from api.v1.auth.auth import Auth
        auth = Auth()
    elif auth_inst == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth_inst == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()


@app.before_request
def before_request() -> str:
    """works on data before request"""
    if auth is None:
        return
    excluded_path = [
            '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'
            ]
    if not auth.require_auth(request.path, excluded_path):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbiden error
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
