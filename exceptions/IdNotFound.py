class IdNotFoundError(Exception):

    def __init__(self, id, message='the id you entered is not in the system: id = '):
        self.id = id
        self.message = message

    def __str__(self):
        return f'IdNotFoundError: {self.message, self.id}'
