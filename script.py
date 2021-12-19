from examer import Examer
from ExamerException import GettingTestError
import codecs

# ======================================

EMAIL = ''
PASSWORD = ''

# =======================================


if __name__ == '__main__':
    ex = Examer(EMAIL, PASSWORD)

    try:
        test = ex.get_test(input('Your link: '))
    except GettingTestError:
        print('Неверная ссылка')
    else:
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
