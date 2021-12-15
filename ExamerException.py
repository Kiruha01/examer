class LoginError(Exception):
    def __init__(self):
        self.message = "Неопознанная ошибка регистрации"
        super().__init__(self.message)


class EmailPasswordError(Exception):
    def __init__(self):
        self.message = "Неверный email или пароль"
        super().__init__(self.message)


class GettingTestError(Exception):
    def __init__(self):
        self.message = "Ошибка в получении теста"
        super().__init__(self.message)


class SignError(Exception):
    def __init__(self):
        self.message = "Ошибка генерации запроса регистрации"
        super().__init__(self.message)


class TeacherError(Exception):
    def __init__(self):
        self.message = "Пользователь не является учителем"
        super().__init__(self.message)
