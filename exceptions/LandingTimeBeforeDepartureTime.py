class LandingTimeBeforeDepartureTimeError(Exception):

    def __init__(self, landing_time, departure_time, message='the landing time must to be after the departure time. '):
        self.landing_time = landing_time
        self.departure_time = departure_time
        self.message = message

    def __str__(self):
        return f'LandingTimeBeforeDepartureTimeError: {self.message}landing time: {self.landing_time}, ' \
               f'departure time: {self.departure_time}'
