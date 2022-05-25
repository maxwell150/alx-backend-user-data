#!/usr/bin/env python3
"""basic Flask app.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """index to display message"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users() -> str:
    """register user"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST to create a new session"""
    form = request.form
    if "email" not in form:
        return jsonify({"message": "email required"}), 400
    elif "password" not in form:
          return jsonify({"message": "password required"}), 400
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if AUTH.valid_login(email, password) is False:
            abort(401)
        else:
            session_id = AUTH.create_session(email)
            response = jsonify({
                "email": email,
                "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """logout"""
    session_id = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(session_id)
    if not usr:
        abort(403)
    AUTH.destroy_session(usr.id)
    return redirect('/')

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """respond to the GET /profile route."""
    session_id = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(session_id)
    if usr:
        return jsonify({"email": usr.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
