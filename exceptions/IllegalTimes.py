class IllegalTimesError(Exception):

    def __init__(self, message='you entered a illegal times: '):
        self.message = message

    def __str__(self):
        return f'IllegalTimesError: {self.message}'