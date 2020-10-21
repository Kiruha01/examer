# Скрипт для поиска ответов тестов Examer
Данный скрипт испльзуется для автоматического поиска ответов тестов Экзамера путём перебора вопросов по этой теме с аккаунта преподавателя. Для использования необходимо сделать насколько подготовительных шагов

### Регистрация учителя
***На данный момент доступен вход на Экзамер только через вк.*** Поэтому создаём новый аккаунт вк (но можно использовать свой). Далее на сайте Examer'а входим через вк и выбираем пункт "Я учитель"

### Установка Python
Данный скрипт написан на python, поэтому скачиваем последнюю версию с [сайта](https://www.python.org/). Следуем инструкциям для вашей ОС.

### Установка зависимостей
Теперь необходимо установить требуемые библиотеки. В папке репозитория находится файл `
requirements.txt`. Открываем коммандную строку или терминал этой папке и вводим 
```bash 
$ pip install -r requirements.txt
```

### Установка логина и пароля
Открываем файл `script.py`. В начале файла необходимо внести логин и пароль от вк для нашего преподавателя:
```python
# ====== Ваши данные здесь ==============

EMAIL = 'TYPE YOUR E-MAIL' # логин
PASSWORD = 'TYPE YOUR PASSWORD' # пароль

# =======================================
```
Далее сохраняет файл и запускаем командой 
```bash
$ python script.py
```
Нас попросят ввести ссылку на тест. Вставляем её и через некоторое время в папке появится файл с ответами `answers.txt`.