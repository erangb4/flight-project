class UsernameAlreadyExistError(Exception):

    def __init__(self, username, message='the user name is already exist. username = '):
        self.username = username
        self.message = message

    def __str__(self):
        return f'UsernameAlreadyExistError: {self.message+self.username}. '
