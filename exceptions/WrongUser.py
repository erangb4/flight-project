class WrongUserError(Exception):

    def __init__(self, username, message='this username is not exist: '):
        self.username = username
        self.message = message

    def __str__(self):
        return f'WrongUserError: {self.message, self.username}'
