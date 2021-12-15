from examer import Examer
import codecs

# ====== Ваши данные здесь ==============

EMAIL = 'hawetoh999@hagendes.com'
PASSWORD = '123456789'

# =======================================


if __name__ == '__main__':
    if EMAIL == 'TYPE YOUR E-MAIL' or PASSWORD == 'TYPE YOUR PASSWORD':
        print("""!!! Вы не ввели ваш логин и пароль для входа на Экзамер.
!!! Откройте файл 'script.py' в текстовом редакторе и измените переменные EMAIL и PASSWORD""")
    else:

        ex = Examer(EMAIL, PASSWORD)

        test = ex.get_test(input('Your link: '))
        f = codecs.open('answers.txt', 'w', 'utf_8_sig')
        print(test.theme, file=f)
        print('Всего баллов:', test.score, file=f)
        print('Примерное время на выполнения теста:', test.avg_time, "минут", file=f)
        print('===============\n', file=f)

        for task in test.get_tasks():
            print("Баллов за задание:", task.difficult, file=f)
            print(task.question, file=f)
            print("Ответ:", task.answer, file=f)
            print('---\n', file=f)



        f.close()
