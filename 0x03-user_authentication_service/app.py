#!/usr/bin/env python3
"""basic Flask app.
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """index to display message"""
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
