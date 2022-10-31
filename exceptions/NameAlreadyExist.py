class NameAlreadyExistError(Exception):

    def __init__(self, name, message='the name is already exist. name = '):
        self.name = name
        self.message = message

    def __str__(self):
        return f'NameAlreadyExistError: {self.message+self.name}. '
