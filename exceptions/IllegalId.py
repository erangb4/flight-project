class IllegalIdError(Exception):

    def __init__(self, message='you entered a illegal id.'):
        self.massage = message

    def __str__(self):
        return f'IllegalIdError: {self.massage} '
