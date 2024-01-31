#!/usr/bin/python3
"""Web Flask Module"""
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello():
    """Home route function"""
    return "Hello HBNB!"
