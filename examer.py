import hashlib
from typing import List, Dict

from bs4 import BeautifulSoup
import requests

from ExamerException import *


class Task:
    def __init__(self, task_dict: Dict[str, str]):
        self.id: str = task_dict['id']
        self.question: str = self.__remove_tags(task_dict['task_text'])
        self.difficult: int = self.__convert_dif(task_dict['difficult'])
        self.avg_time: float = float(task_dict['avg_time'])
        self.answer = None

    @staticmethod
    def __remove_tags(text: str) -> str:
        soup = BeautifulSoup(text, 'html.parser')
        return soup.text

    @staticmethod
    def __convert_dif(grade: str) -> int:
        if grade == 'easy':
            return 1
        elif grade == 'normal':
            return 2
        else:
            return 3


class ExamerTest:
    def __init__(self, test_dict: Dict):
        self.theme: str = test_dict['title']
        self.id_test: str = str(test_dict['scenarioId'])
        self.score: str = str(test_dict['score'])
        self.tasks: Dict[str, Task] = {}
        self.avg_time = 0
        for task in test_dict['tasks']:
            t = Task(task)
            self.tasks[t.id] = t
            self.avg_time += t.avg_time
        self.unprocessed_tasks_id: List[str] = list(self.tasks.keys())

        self.avg_time = round(self.avg_time / 30)

    def get_tasks(self) -> List[Task]:
        return list(self.tasks.values())


class Examer(object):
    def __init__(self, email: str, password: str):
        self.BASE_URL = "https://examer.ru/"
        self.SIGN_POSTFIX = 'Ic8_31'
        self.session = requests.session()
        if email and password:
            self.auth(email, password)

    def auth(self, email: str, password: str):
        response = self.session.get(self.BASE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        token = soup.find(id='login-form').find('input', attrs={"name": "_token"})["value"]
        params = self.prepare_auth_request_params(email, password, token)

        headers = {"Referer": self.BASE_URL, "Cookie": response.headers['Set-Cookie']}
        response = self.session.post(self.BASE_URL + 'api/v2/login', headers=headers, data=params)
        if not response.json()['success']:
            if response.json()['error'] == 3:
                raise EmailPasswordError()
            elif response.json()['error'] == 101:
                raise SignError()
            else:
                raise LoginError()

    def prepare_auth_request_params(self, email: str, password: str, token: str) -> Dict[str, str]:
        data = {
            '_mail': email,
            '_pass': password,
            "_token": token,
            "source_reg": 'login_popup'
        }
        string = ''.join(sorted(data.values())) + self.SIGN_POSTFIX
        data['s'] = hashlib.md5(string.encode('utf-8')).hexdigest()
        return data

    def get_questions(self, link: str) -> ExamerTest:
        tasks = self.session.get(self.BASE_URL + 'api/v2/teacher/test/student/' + link).json()
        if 'error' in tasks:
            raise GettingTestError()
        return ExamerTest(tasks['test'])

    def generate_test(self, test_id: str, test_theme: str) -> Dict:
        payload = {'sid': '3', 'scenario': '1', 'id': test_id, 'title': test_theme, 'easy': '6', 'normal': '7',
                   'hard': '7'}
        return self.session.post(url='https://teacher.examer.ru/api/v2/teacher/test',
                                 data=payload).json()

    def get_test(self, link: str) -> ExamerTest:
        test_id = link.split('/')[-1]
        test = self.get_questions(test_id)

        while len(test.unprocessed_tasks_id):
            data = self.generate_test(test.id_test, test.theme)
            for task in data['tasks']:
                if task['id'] in test.unprocessed_tasks_id:
                    test.tasks[task['id']].answer = task['answer']
                    test.unprocessed_tasks_id.remove(task['id'])
        return test
