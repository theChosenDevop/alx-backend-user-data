#!/usr/bin/env python3
"""
End to End (E2E) Integration Testing
"""
import requests

base_url: str = 'http://0.0.0.0:5000/%s'


def register_user(email: str, password: str) -> None:
    """Test user if it exist or not with the json output
       Args:
            email [str]: user email
            password [str]: user password
       Returns: None
    """
    url = base_url % 'users'
    payload = [('email', email), ('password', password)]
    response = requests.post(url, data=payload)
    # if the user is a new user with email or password
    expected_json = {"email": email, "message": "user created"}
    assert response.json() == expected_json
    assert response.status_code == 200

    # if user already exist
    response = requests.post(url, data=payload)
    expected_json = {"message": "email already registered"}
    assert response.json == expected_json
    assert response.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login endpoint with wrong password
        Args:
            email [str]: user email
            password [str]: user password
        Returns: None
    """
    url = base_url % 'sessions'
    payload = {"email": email, "password": password}
    expected = {'error': 'Unauthorized'}
    response = requests.post(url, data=payload)
    assert response.status_code == 401
    assert response.json() == expected
    assert not response.cookies


def log_in(email: str, password: str) -> str:
    """Test login endpoint with  password
        Args:
            email [str]: user email
            password [str]: user password
        Returns: string
    """
    url = base_url % 'sessions'
    payload = {'email': email, 'password': password}
    expected = {"email": email, "message": "logged in"}
    response = requests.post(url, data=payload)
    session_id = response.cookies.get('session_id')
    assert response.json() == expected
    assert response.status_code == 200
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Test unlogged user profile"""
    url = base_url % 'profile'
    response = requests.post(url, cookies=dict())
    expected = {"error": "Forbidden"}
    assert response.status_code == 403
    assert response.json() == expected


def profile_logged(session_id: str) -> None:
    """Test user logged in profile"""
    url = base_url % 'profile'
    response = requests.post(url, cookies=dict(session_id=session_id))
    assert response.status_code == 200
    assert response.json().get('email') is not None


def log_out(session_id: str) -> None:
    """Test log out feature of user"""
    url = base_url % 'sessions'
    response = requests.delete(url, cookies=dict(session_id=session_id))
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test reset password token"""
    url = base_url % 'reset_password'
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reset_token" in data
    assert data["email"] == email
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update password"""
    url = base_url % 'reset_password'
    # update password if found
    expected = {"email": email, "message": "Password updated"}
    payload = {
            "email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=payload)
    assert response.status_code == 200
    assert response.json() == expected


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
