#!/usr/bin/env python3
"""basic Flask app.
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
Auth = Auth()


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
        user = Auth.register_user(email, password)
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
        if Auth.valid_login(email, password) is False:
            abort(401)
        else:
            session_id = Auth.create_session(email)
            response = jsonify({
                "email": email,
                "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
