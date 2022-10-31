class NegativeInputError(Exception):

    def __init__(self, message='you entered a negative number: '):
        self.message = message

    def __str__(self):
        return f'NegativeInputError: {self.message}'
