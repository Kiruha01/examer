from flask import Flask, request, json
import main


app = Flask(__name__)


@app.route('/')
def hanr():
    return 'ok'

@app.route('/', methods=['POST'])
def handler():
    data = json.loads(request.data)
    if data['type'] == 'confirmation':
        return 'bf65672b'
    elif data["type"] == "message_new":
        user_id = data['object']['user_id']
        text = data['object']['body']
        main.main(user_id, text)
        return 'ok'


