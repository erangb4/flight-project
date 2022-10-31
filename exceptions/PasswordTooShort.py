class PasswordTooShortError(Exception):

    def __init__(self, message='the password must to be with at least 6 characters. '):
        self.message = message

    def __str__(self):
        return f'PasswordTooShortError: {self.message}. '
