import time

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/long_task')
def long_task():
    time.sleep(10)
    return jsonify(message='We did it!')
