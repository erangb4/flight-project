class NoMoreTicketsError(Exception):

    def __init__(self, flight_id, message='there is no more tickets to this flight: Flight_id = '):
        self.flight_id = flight_id
        self.message = message

    def __str__(self):
        return f'NoMoreTicketsError: {self.message+self.flight_id}. '
