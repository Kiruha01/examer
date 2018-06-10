token = '6be1dc7d81306eaa2394e1b512fa2ce7b6ef4432aef65ac1523513ec6495e2b753fbf06afc305d565ce6b'

import vk_api
from examer import Examer

vk = vk_api.vk_api.VkApi(token=token)

ex = Examer('arkadiy@p33.org', 'zabylkto01')

memory = {}

def get_last_id():
    data = vk.method('messages.get', {'count': 1})['items']
    return data[0]['id']

def main(id, text):
    global ex
    global memory
    if text == 'Привет':
        return vk.method('messages.send', {'user_id': id, 'message': 'Кидай ссылку на тест и я решу его за тебя'})
    elif text == 'reset' and str(id) == '276820555':
        memory = {}
        vk.method('messages.send', {'user_id': '276820555', 'message': 'ok'})
    else:
        link = text.split('/')[-1]
        if link in memory:
            for msg in memory[link]:
                vk.method('messages.send', {'user_id': id, 'message': msg})
        else:
            
            ex.set_link(text)
            try:
                ex.start()
            except ArithmeticError:
                vk.method('messages.send', {'user_id': id, 'message': 'Invalid Link'})
            else:
                ex.format_text()
                list_ = []
                for task_id in ex.list_of_task:
                    list_.append(task_id['question'] + '\nОтвет: ' + task_id['answer'])
                memory[link] = list_
                main(id, text)
    


