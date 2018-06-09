from flask import Flask, request, Response


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handler():
    if data['type'] == 'confirmation':
        return 'bf65672b'

