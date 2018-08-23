from flask import Flask, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = b'q\xe1`\xef\xb4\xe6I\x9e)Jt\xc3\x97\x9b\xefB'

from app import routes
