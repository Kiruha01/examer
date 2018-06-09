from flask import Flask, request, json


app = Flask(__name__)


@app.route('/')
def hanr():
    return 'ok'

@app.route('/', methods=['POST'])
def handler():
    data = json.loads(request.data)
    if data['type'] == 'confirmation':
        return 'bf65672b'

