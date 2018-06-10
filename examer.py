import mechanicalsoup
from json import loads

class Examer(object):
    def __init__(self, login=None, password=None):
        self.list_of_task = []
        if login and password:
            self.auth(login, password)


    def auth(self, login, passw):
        self.person = mechanicalsoup.StatefulBrowser()
        self.person.open('https://examer.ru/login/vkontakte')
        self.person.select_form() # Выбор формы с регистрацией {id="login_submit"}
    #   print(br.get_current_form().print_summary()) # !!!!
        self.person['email'] = login
        self.person['pass'] = passw      # ввод данных
        self.person.submit_selected()    # Submit'им форму


    def set_link(self, link):
        self.link = link.split('/')[-1]


    def start(self, *arg, num_of_iter=100):
        list_of_pull = []
        dict_of_task = {}
        tasks = self.person.get('https://teacher.examer.ru/api/v2/teacher/test/student/' + self.link)
        tasks = loads(tasks.text)
        if 'error' in tasks:
            raise ArithmeticError
        self.theme = tasks['test']['title'] # Тема теста
        self.id_test = str(tasks['test']['scenarioId']) # ID теста

        for z in tasks['test']['tasks']: # Перебор в заданиях 
            dict_of_task[z['id']] = {'question': z['task_text'], 'answer': None}
            list_of_pull.append(z['id']) # Добавление ID в список необработанных

        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        
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
        print(1)
        for task in self.list_of_task:
            s = task['question']
            i = 0
            while s.find('<') != -1 or s.find('>') != -1:
                pattern = s[s.find('<') : s.find('>')+1]
                #print(pattern)

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
            # while s.find('&laquo;') != -1 or s.find('&raquo;') != -1 or s.find('&mdash;') != -1:
            #     if s.find('&laquo;') != -1:
            #         s = s.replace('&laquo;', '')
            #     if s.find('&raquo;') != -1:
            #         s = s.replace('&raquo;', '')
            #     if s.find('&mdash;') != -1:
            #         s = s.replace('&mdash;', '-')
            task['question'] = s
        
                    

if __name__ == '__main__':
    ex = Examer('arkadiy@p33.org', 'zabylkto01')
    err = True
    while err:
        ex.set_link(input('Your link: '))

        try:
            ex.start()
        except ArithmeticError:
            pass
        else:
            err = False
    ex.format_text()
    f = open('aaa.txt', 'w')
    for task_id in ex.list_of_task:

        print(task_id['question'], task_id['answer'], file=f)
        print('===============', file=f)
    f.close()


