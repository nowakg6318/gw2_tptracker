from flask import Flask, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

from app import routes
