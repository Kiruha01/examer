class LoginError(Exception):
    def __init__(self):
        self.message = "Неопознанная ошибка регистрации"


class EmailPasswordError(Exception):
    def __init__(self):
        self.message = "Неверный email или пароль"


class GettingTestError(Exception):
    def __init__(self):
        self.message = "Ошибка в получении теста"


class SignError(Exception):
    def __init__(self):
        self.message = "Ошибка генерации запроса регистрации"
