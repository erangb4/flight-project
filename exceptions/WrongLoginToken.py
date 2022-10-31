class WrongLoginTokenError(Exception):

    def __init__(self, login_token, message='You are entering details that do not match the corrected login token: '):
        self.login_token = login_token
        self.message = message

    def __str__(self):
        return f'WrongLoginTokenError: {self.message, self.login_token}'
