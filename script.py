from examer import Examer

# ====== Ваши данные здесь ==============

EMAIL = 'TYPE YOUR E-MAIL'
PASSWORD = 'TYPE YOUR PASSWORD'

# =======================================


if __name__ == '__main__':
    if EMAIL == 'TYPE YOUR E-MAIL' or PASSWORD == 'TYPE YOUR PASSWORD':
        print("""!!! Вы не ввели ваш логин и пароль для входа на Экзамер.
!!! Откройте файл 'script.py' в текстовом редакторе и измените переменные EMAIL и PASSWORD""")
    else:

        ex = Examer(EMAIL, PASSWORD)
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
        f = open('answers.txt', 'w')
        for task_id in ex.list_of_task:

            print(task_id['question'], task_id['answer'], file=f)
            print('===============', file=f)
        f.close()