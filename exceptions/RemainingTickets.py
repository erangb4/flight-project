class RemainingTicketsError(Exception):

    def __init__(self, message='remaining tickets the remaining tickets must be at least 50 tickets.'):
        self.message = message

    def __str__(self):
        return f'NegativeRemainingTicketsError: {self.message}'
