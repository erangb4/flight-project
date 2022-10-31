class OriginCountryAndDestinationCountryAreTheSameError(Exception):

    def __init__(self, origin_country, des_country,
                 message='the origin country and the destination country cant be the same'):
        self.origin_country = origin_country
        self.des_country = des_country
        self.message = message

    def __str__(self):
        return f'OriginCountryAndDestinationCountryAreTheSameError: {self.message}: ' \
               f'origin country = {self.origin_country}, destination country = {self.des_country}.'
