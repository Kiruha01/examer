import mechanicalsoup
from json import loads


def convertDif(grade):
    if grade == 'easy':
        return 1
    elif grade == 'normal':
        return 2
    else:
        return 3


class Examer(object):
    def __init__(self, login=None, password=None):
        self.list_of_task = []
        if login and password:
            self.auth(login, password)
        self.score = 'НЕТДАННЫХ'


    def auth(self, login, passw):
        self.person = mechanicalsoup.StatefulBrowser()
        self.person.open('https://examer.ru/login/vkontakte')
        self.person.select_form() # Выбор формы с регистрацией {id="login_submit"}
        self.person['email'] = login
        self.person['pass'] = passw      # ввод данных
        self.person.submit_selected()    # Submit'им форму


    def set_link(self, link):
        self.link = link.split('/')[-1]


    def start(self, *arg, num_of_iter=100):
        list_of_pull = []
        dict_of_task = {}
        print('Get tasks')
        tasks = self.person.get('https://teacher.examer.ru/api/v2/teacher/test/student/' + self.link)
        tasks = loads(tasks.text)
        if 'error' in tasks:
            raise ArithmeticError
        self.theme = tasks['test']['title'] # Тема теста
        self.id_test = str(tasks['test']['scenarioId']) # ID теста
        self.score = str(tasks['test']['score'])
        self.time = 0
        

        for z in tasks['test']['tasks']: # Перебор в заданиях 
            dict_of_task[z['id']] = {'question': '🌚'*convertDif(z['difficult']) + '\n' + z['task_text'], 'answer': None}
            self.time += float(z['avg_time'])
            list_of_pull.append(z['id']) # Добавление ID в список необработанных

        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        print('Get answers')
        payload = {'sid': '3', 'scenario': '1', 'id': self.id_test, 'title': self.theme, 'easy': '6', 'normal': '7', 'hard': '7'}
        iterations = 0
        while len(list_of_pull) and iterations <= num_of_iter: # Защита от невозможности найти вопрос
            iterations += 1
            res = self.person.post(url='https://teacher.examer.ru/api/v2/teacher/test', data=payload) # Получаем данные с ответами
            data = loads(res.text) # Конвертируем

            for task in data['tasks']:                                      # В каждом вопросе ищем
                if task['id'] in list_of_pull:                              # Если ID задания в пуле
                    dict_of_task[task['id']]['answer'] = task['answer']     # то отмечаем ответ
                    list_of_pull.remove(task['id'])                         # и удаляем из пула

        for ids in dict_of_task:
            self.list_of_task.append(dict_of_task[ids])


    def format_text(self):
        print('Format text')
        for task in self.list_of_task:
            s = task['question']
            i = 0
            while s.find('<') != -1 or s.find('>') != -1:
                pattern = s[s.find('<') : s.find('>')+1]

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
