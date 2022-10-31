class PhoneNumberAlreadyExistError(Exception):

    def __init__(self, phone, message='the phone number is already exist. phone number = '):
        self.phone = phone
        self.message = message

    def __str__(self):
        return f'PhoneNumberAlreadyExistError: {self.message + self.phone}. '
