from abc import ABC, abstractmethod
from datetime import datetime
from LoginToken import LoginToken
from tables.AirlineCompany import AirlineCompany
from tables.Country import Country
from tables.Flight import Flight
from exceptions.IdNotFound import IdNotFoundError
from exceptions.IllegalId import IllegalIdError
from Logger import Logger
from exceptions.WrongData import WrongDataError


class FacadeBase(ABC):

    @abstractmethod
    def __init__(self, repo, login_token=LoginToken(id=None, name='Anonymous', role='Anonymous')):
        self.logger = Logger.get_instance()
        self._login_token = login_token
        self.repo = repo

    @property
    def login_token(self):
        return self._login_token

    def get_all_flights(self):
        return self.repo.get_all(Flight)

    def get_flight_by_id(self, id):
        if not type(id) is int or id < 0:
            self.logger.logger.error(f'{self.login_token} tried to get flight by id but the id is illegal.')
            raise IllegalIdError(id)
        if self.repo.get_by_id(Flight, id) is None:
            self.logger.logger.error(f'{self.login_token} tried to get flight by id but the id is did not found.')
            raise IdNotFoundError(id)
        return self.repo.get_by_id(Flight, id)

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, departure_date):
        if not type(origin_country_id) is int or not type(destination_country_id) is int:
            self.logger.logger.error(f'{self.login_token} tried to get flights by parameters but origin_country_id or '
                                     f'destination_country_id is illegal.')
            raise IllegalIdError()
        if not isinstance(departure_date, datetime):
            self.logger.logger.error(f'{self.login_token} tried to get flights by parameters but the departure date is '
                                     f'illegal')
            raise WrongDataError
        return self.repo.get_by_condition(Flight, lambda query: query.filter(Flight.origin_country_id ==
                    origin_country_id, Flight.destination_country_id == destination_country_id, Flight.departure_time ==
                    departure_date).all())

    def get_all_airlines(self):
        return self.repo.get_all(AirlineCompany)

    def get_airline_by_id(self, id):
        if not type(id) is int or id < 0:
            self.logger.logger.error(f'{self.login_token} tried to get airline by id but the id is illegal.')
            raise IllegalIdError(id)
        if self.repo.get_by_id(Flight, id) is None:
            self.logger.logger.error(f'{self.login_token} tried to get airline by id but the id is not exist.')
            raise IdNotFoundError(id)
        return self.repo.get_by_id(AirlineCompany, id)

    def get_all_countries(self):
        return self.repo.get_all(Country)

    def get_country_by_id(self, id):
        if not type(id) is int or id < 0:
            self.logger.logger.error(f'{self.login_token} tried to get country by id but the id is illegal.')
            raise IllegalIdError()
        if self.repo.get_by_id(Flight, id) is None:
            self.logger.logger.error(f'{self.login_token} tried to get country by id but the id is illegal.')
            raise IdNotFoundError(id)
        return self.repo.get_by_id(Country, id)
