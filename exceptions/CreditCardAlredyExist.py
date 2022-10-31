class CreditCardAlreadyExistError(Exception):

    def __init__(self, credit_card, message='the credit_card is already exist. credit_card = '):
        self.credit_card = credit_card
        self.message = message

    def __str__(self):
        return f'CreditCardAlreadyExistError: {self.message + self.credit_card}. '
