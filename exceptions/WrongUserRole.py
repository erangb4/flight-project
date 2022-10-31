class WrongUserRoleError(Exception):

    def __init__(self, message='wrong user role '):
        self.message = message

    def __str__(self):
        return f'WrongUserError: {self.message}'
