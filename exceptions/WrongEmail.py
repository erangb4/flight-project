class WrongEmailError(Exception):

    def __init__(self, email, message='this email all ready: '):
        self.email = email
        self.message = message

    def __str__(self):
        return f'WrongEmailError: {self.message, self.email}'
