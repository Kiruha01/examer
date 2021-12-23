import asyncio
import hashlib
from typing import List, Dict

import aiohttp
from bs4 import BeautifulSoup
import requests
from concurrent import futures

from asyncio import FIRST_EXCEPTION

from ExamerException import *
import time


class Task:
    """
    Структура, описывающая задание

    :field id: str - ID задания
    :field question: str - текст задания
    :field difficult: int - баллы за задание (1, 2 или 3)
    :field avg_time: float - время на выполнение
    :field answer: str - правильный ответ

    """

    def __init__(self, task_dict: Dict[str, str]):
        self.id: str = task_dict['id']
        self.question: str = self.__remove_tags(task_dict['task_text'])
        self.difficult: int = self.__convert_dif(task_dict['difficult'])
        self.avg_time: float = float(task_dict['avg_time'])
        self.answer = "No answer"

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
    """
        Структура, описывабщая тест

        :field theme: str - тема теста
        :field score: str - возможное количество баллов за тест
        :field tasks: Dist[str, Task] - словарь заданий вида ("task_id": Task)
        :field avg_time: int - примерное время выполнения теста
    """

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
        """
        Получить список вопросов
        :return: List[Task]
        """
        return list(self.tasks.values())


class Examer(object):
    def __init__(self, email: str, password: str):
        """
        Основной класс для взаимодействия с API examer.

        :param email: str - email для входа в аккаунт
        :param password: str - пароль для входа в аккаунт

        :raises EmailPasswordError: неверный логин или пароль
        :raises LoginError: неопознанная ошибка входа
        :raises SignError: ошибка отправки запроса решистрации
        :raises TeacherError: пользователь не является учителем
        """
        self.MAX_REQUESTS = 10
        self.BASE_URL = "https://examer.ru/"
        self.SIGN_POSTFIX = 'Ic8_31'
        self.session = requests.session()
        if email and password:
            self.auth(email, password)

    def auth(self, email: str, password: str):
        """
        Метод входа в аккаунт
        :param email: str
        :param password: str
        :return: None

        :raises EmailPasswordError: неверный логин или пароль
        :raises LoginError: неопознанная ошибка входа
        :raises SignError: ошибка отправки запроса решистрации
        :raises TeacherError: пользователь не является учителем
        """
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
        response = self.session.get(self.BASE_URL + 'api/v2/user').json()
        if not response['profile']['is_teacher']:
            raise TeacherError()

    def get_test(self, link: str) -> ExamerTest:
        """
        Метод получения ответов на тест по ссылке.
        :param link: str - ссылка на тест
        :return: ExamerTest
        """
        test_id = link.split('/')[-1]
        test = self.get_questions(test_id)

        while len(test.unprocessed_tasks_id):
            data = self.generate_test(test.id_test, test.theme)
            for task in data['tasks']:
                if task['id'] in test.unprocessed_tasks_id:
                    test.tasks[task['id']].answer = task['answer']
                    test.unprocessed_tasks_id.remove(task['id'])
        return test

    def async_get_test(self, link: str):
        async def gen_test(test: ExamerTest, session):
            payload = {'sid': '3', 'scenario': '1', 'id': test.id_test, 'title': test.theme, 'easy': '12', 'normal': '12',
                       'hard': '12'}

            async with session.post('https://teacher.examer.ru/api/v2/teacher/test', data=payload) as resp:
                data = await resp.json()
                for task in data['tasks']:
                    if task['id'] in test.unprocessed_tasks_id:
                        test.tasks[task['id']].answer = task['answer']
                        test.unprocessed_tasks_id.remove(task['id'])
                if len(test.unprocessed_tasks_id) == 0:
                    raise StopIteration

        async def asynchronous(test: ExamerTest):
            async with aiohttp.ClientSession(cookies=self.session.cookies.get_dict()) as session:
                tasks = [asyncio.create_task(gen_test(test, session))
                         for i in range(self.MAX_REQUESTS)]

                _, pendings = await asyncio.wait(tasks, return_when=FIRST_EXCEPTION)
                for p in pendings:
                    p.cancel()


        test_id = link.split('/')[-1]
        test = self.get_questions(test_id)

        i = 0
        while len(test.unprocessed_tasks_id):
            print('new')
            asyncio.run(asynchronous(test))
        return test

    def prepare_auth_request_params(self, email: str, password: str, token: str) -> Dict[str, str]:
        """
        Подготовка параметров для регистрации и добавление подписи.
        :param email: str - email для входа
        :param password: str - пароль для входа
        :param token: str - токен с формы регистрации
        :return: Dict[str, str]
        """
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
        """
        Получение вопросов теста.
        :param link: str - идентификатор теста из ссылки
        :return: ExamerText
        """
        tasks = self.session.get(self.BASE_URL + 'api/v2/teacher/test/student/' + link).json()
        if 'error' in tasks:
            raise GettingTestError()
        return ExamerTest(tasks['test'])

    def generate_test(self, test_id: str, test_theme: str) -> Dict:
        """
        Генерация теста из случайных вопросов по выбранной теме
        :param test_id: str - ID предмета
        :param test_theme: str - название темы теста
        :return: Dict
        """
        payload = {'sid': '3', 'scenario': '1', 'id': test_id, 'title': test_theme, 'easy': '12', 'normal': '12',
                   'hard': '12'}
        return self.session.post(url='https://teacher.examer.ru/api/v2/teacher/test',
                                 data=payload).json()


if __name__ == "__main__":
    ex = Examer('hawetoh999@hagendes.com', '123456789')
    print("starting")
    time_s = time.monotonic()
    print(ex.get_test('https://t.examer.ru/f9afa'))
    print("Sync ", time.monotonic() - time_s)
    time_s = time.monotonic()
    print(ex.async_get_test('https://t.examer.ru/f9afa'))
    print("Async ", time.monotonic() - time_s)
