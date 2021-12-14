class LoginError(Exception):
    def __init__(self):
        self.message = "Неопознанная ошибка регистрации"


class EmailPasswordError(Exception):
    def __init__(self):
        self.message = "Неверный email или пароль"


class NotTeacher(Exception):
    def __init__(self):
        self.message = "Пользователь не является учителем"


class SignError(Exception):
    def __init__(self):
        self.message = "Ошибка генерации запроса регистрации"
