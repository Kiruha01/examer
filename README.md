# Скрипт для поиска ответов тестов Examer
Данный скрипт используется для автоматического поиска ответов тестов Экзамера путём перебора вопросов по этой теме с аккаунта преподавателя. Для использования необходимо сделать насколько подготовительных шагов

## Подготовка
### Установка Python
Данный скрипт написан на python, поэтому скачиваем последнюю версию с [сайта](https://www.python.org/). Следуем инструкциям для вашей ОС.

### Установка зависимостей
Теперь необходимо установить требуемые библиотеки. В папке репозитория находится файл `
requirements.txt`. Открываем коммандную строку или терминал этой папке и вводим 
```bash 
$ pip install -r requirements.txt
```

### Регистрация учителя
Регистрируем аккаунт на examer и после регистрации выбираем опцию **"Я учитель"**.

## Простой пример
В файле `script.py` вставляем логин и пароль от только что созданного аккаунта нашего преподавателя:
```python
# =======================================

EMAIL = 'TYPE YOUR E-MAIL'
PASSWORD = 'TYPE YOUR PASSWORD'

# =======================================
```
Далее сохраняем файл и запускаем командой 
```bash
$ python script.py
```
Нас попросят ввести ссылку на тест. Вставляем её и через некоторое время в папке появится файл с ответами `answers.txt`.

## Использование
### Вход в аккаунт
```python
from examer import Examer

ex = Examer('example@example.com', 'password')
```
В случае ошибки поднимаются исключения:
* `ExamerException.LoginError` - неопознанная ошибка регистрации. 
* `ExamerException.EmailPasswordError` - неверный логин или пароль. 
* `ExamerException.SignError` - Ошибка генерации запроса регистрации (неверные куки, подпись запроса и прочее)
* `ExamerException.TeacherError` - Данный пользователь не является учителем

### Получение теста с ответами
```python
link = "https://t.examer.ru/f9afa"
test = ex.get_test(link)
```
В случае ошибки поднимаются исключения:
* `ExamerException.GettingTestError` - ошибка получения теста. Осноная причина - неверныая ссылка на тест

#### Работа с тестом
```python
# Тема теста
test.theme
# ID теста
test.id_test
# Возможное число баллов за тест
test.score
# Примерное время на выполнение теста
test.avg_time

for task in test.get_tasks():
    # Текст вопроса
    task.question
    # Правильный ответ
    task.answer
    # Баллов за вопрос
    task.difficult

```
