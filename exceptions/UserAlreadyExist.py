class UserAlreadyExistError(Exception):

    def __init__(self, user, message='the user is already exist. user = '):
        self.user = user
        self.message = message

    def __str__(self):
        return f'UserAlreadyExistError: {self.message + self.user}. '
