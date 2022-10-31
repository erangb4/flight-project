class WrongDataError(Exception):

    def __init__(self, message='this data is not valid '):
        self.message = message

    def __str__(self):
        return f'WrongEmailError: {self.message,}'
