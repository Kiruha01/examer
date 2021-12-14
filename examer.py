import hashlib

from bs4 import BeautifulSoup
import requests
from json import loads

from ExamerException import *


def convertDif(grade):
    if grade == 'easy':
        return 1
    elif grade == 'normal':
        return 2
    else:
        return 3


class Examer(object):
    def __init__(self, login=None, password=None):
        self.BASE_URL = "https://examer.ru/"
        self.SIGN_POSTFIX = 'Ic8_31'
        self.session = requests.session()
        self.list_of_task = []
        if login and password:
            self.auth(login, password)
        self.score = 'НЕТДАННЫХ'
        self.time = 0

    def auth(self, email, password):
        response = self.session.get(self.BASE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(id='login-form').find('input', attrs={"name": "_token"})["value"]
        params = self.prepare_auth_request_params(email, password, token)
        print('params=', params)

        headers = {"Referer": self.BASE_URL, "Cookie": response.headers['Set-Cookie']}
        response = self.session.post(self.BASE_URL + 'api/v2/login', headers=headers, data=params)
        print(response.json())
        if not response.json()['success']:
            if response.json()['error'] == 3:
                raise EmailPasswordError()
            elif response.json()['error'] == 101:
                raise SignError()
            else:
                raise LoginError()

    @staticmethod
    def prepare_auth_request_params(email, password, token):
        data = {
            '_mail': email,
            '_pass': password,
            "_token": token,
            "source_reg": 'login_popup'
        }
        string = ''.join(sorted(data.values())) + 'Ic8_31'
        data['s'] = hashlib.md5(string.encode('utf-8')).hexdigest()
        return data

    def set_link(self, link):
        self.link = link.split('/')[-1]

    def start(self, *arg, num_of_iter=100):
        list_of_pull = []
        dict_of_task = {}
        print('Get tasks')
        tasks = self.session.get('https://teacher.examer.ru/api/v2/teacher/test/student/' + self.link)
        tasks = loads(tasks.text)
        if 'error' in tasks:
            raise ArithmeticError
        self.theme = tasks['test']['title']  # Тема теста
        self.id_test = str(tasks['test']['scenarioId'])  # ID теста
        self.score = str(tasks['test']['score'])

        for z in tasks['test']['tasks']:  # Перебор в заданиях
            dict_of_task[z['id']] = {'question': '🌚' * convertDif(z['difficult']) + '\n' + z['task_text'],
                                     'answer': None}
            self.time += float(z['avg_time'])
            list_of_pull.append(z['id'])  # Добавление ID в список необработанных

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        print('Get answers')
        payload = {'sid': '3', 'scenario': '1', 'id': self.id_test, 'title': self.theme, 'easy': '6', 'normal': '7',
                   'hard': '7'}
        iterations = 0
        while len(list_of_pull) and iterations <= num_of_iter:  # Защита от невозможности найти вопрос
            iterations += 1
            res = self.session.post(url='https://teacher.examer.ru/api/v2/teacher/test',
                                   data=payload)  # Получаем данные с ответами
            data = loads(res.text)  # Конвертируем

            for task in data['tasks']:  # В каждом вопросе ищем
                if task['id'] in list_of_pull:  # Если ID задания в пуле
                    dict_of_task[task['id']]['answer'] = task['answer']  # то отмечаем ответ
                    list_of_pull.remove(task['id'])  # и удаляем из пула

        for ids in dict_of_task:
            self.list_of_task.append(dict_of_task[ids])

    def format_text(self):
        print('Format text')
        for task in self.list_of_task:
            s = task['question']
            i = 0
            while s.find('<') != -1 or s.find('>') != -1:
                pattern = s[s.find('<'): s.find('>') + 1]

                if pattern == '<li>':
                    i += 1
                    count = 1
                    rep = str(i) + ') '
                elif pattern == '':
                    break
                else:
                    rep = ''
                    count = 999

                s = s.replace(pattern, rep, count)
            task['question'] = s
