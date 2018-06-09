from flask import Flask, request, json
import main


app = Flask(__name__)
id_last = main.get_last_id()


@app.route('/')
def hanr():
    return 'ok'

@app.route('/', methods=['POST'])
def handler():
    global id_last
    data = json.loads(request.data)
    if data['type'] == 'confirmation':
        return 'bf65672b'
    elif data['object']['id'] <= id_last:
        return 'ok'
    elif data["type"] == "message_new":
        user_id = data['object']['user_id']
        text = data['object']['body']
        id_last = main.main(user_id, text)
        return 'ok'


