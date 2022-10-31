from datetime import datetime, timedelta
#from project.facades.AnonymousFacade import *
from tables.AirlineCompany import AirlineCompany
from tables.Country import Country
from tables.Flight import Flight
from facades.FacadeBase  import FacadeBase
from exceptions.NameAlreadyExist import NameAlreadyExistError
from exceptions.OriginCountryAndDestinationCountryAreTheSame import \
    OriginCountryAndDestinationCountryAreTheSameError
from exceptions.LandingTimeBeforeDepartureTime import LandingTimeBeforeDepartureTimeError
from exceptions.RemainingTickets import RemainingTicketsError
from exceptions.IdNotFound import IdNotFoundError
from exceptions.IllegalId import IllegalIdError
from exceptions.WrongLoginToken import WrongLoginTokenError
from exceptions.WrongData import WrongDataError


class AirlineFacade(FacadeBase):

    def __init__(self, repo, login_token):
        self.repo = repo
        super().__init__(repo)
        self._login_token = login_token

    def get_flights_by_airline(self):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(f'{self.login_token} tried to use the function of airline company')
            raise WrongLoginTokenError(self.login_token.id)
        return self.repo.get_flights_by_something(Flight.airline_company_id, self.login_token.id)

    def get_country_by_id(self, id):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(f'{self.login_token} tried to use the function of airline company')
            raise WrongLoginTokenError(self.login_token.id)
        if not type(id) is int:
            self.logger.logger.error(f'{self.login_token} tried to get country with illegal id')
            raise IllegalIdError(id)
        if self.repo.get_by_id(Flight, id) is None:
            self.logger.logger.error(f'{self.login_token} tried to get country that not exist')
            raise IdNotFoundError(id)
        return self.repo.get_by_id(Country, id)

    def update_airline(self, airline):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(f'{self.login_token} tried to use the function of airline company')
            raise WrongLoginTokenError(self.login_token.id)
        current_airline = self.repo.get_by_id(AirlineCompany, airline.id)
        if current_airline is None:
            self.logger.logger.error(f'{self.login_token} tried to update a airline with wrong id')
            raise IdNotFoundError(airline.id)
        if self.login_token.id != current_airline.id:
            self.logger.logger.error(f'{self.login_token} tried to update a airline that not belong to him.')
            raise WrongLoginTokenError(self.login_token.id)
        if self.repo.get_airline_by_something(AirlineCompany.name, airline.name) is not None and \
                self.repo.get_airline_by_something(AirlineCompany.name, airline.name) != current_airline.name:
            self.logger.logger.error(f'{self.login_token} tried to update airline with name that already exist.')
            raise NameAlreadyExistError(airline.name)
        if self.repo.get_by_id(Country, airline.country_id) is None:
            self.logger.logger.error(f'{self.login_token} tried to update airline with country_id that not exist.')
            raise IdNotFoundError(airline.country_id)
        self.repo.update_by_id(AirlineCompany, AirlineCompany.id, {AirlineCompany.name: airline.name,
                                                                   AirlineCompany.country_id: airline.country_id})

    def update_flight(self, flight):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(f'{self.login_token} tried to use the function of airline company')
            raise WrongLoginTokenError(self.login_token.id)
        current_flight = self.repo.get_by_id(AirlineCompany, flight.id)
        if current_flight is None:
            self.logger.logger.error(f'{self.login_token} tried to update a flight with wrong id')
            raise IdNotFoundError(flight.id)
        if not isinstance(flight, Flight):
            self.logger.logger.error(f'{self.login_token} tried to update flight but the flight {flight} is not a '
                                     f'Flight object.')
            raise WrongDataError
        if self.login_token.id != flight.airline_company_id:
            self.logger.logger.error(f'{self.login_token} tried to update flight that did not belong to the current '
                                     f'airline company')
            raise WrongLoginTokenError(self.login_token.id)
        if flight.destination_country_id == flight.origin_country_id:
            self.logger.logger.error(f'{self.login_token} tried to update flight but but the origin country and the '
                                     f'destination country are the same')
            raise OriginCountryAndDestinationCountryAreTheSameError(flight.origin_country_id,
                                                                    flight.destination_country_id)
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            self.logger.logger.error(f'{self.login_token} tried to update flight but the departure time and the landing'
                                     f' time must be a datetime object.')
            raise WrongDataError
        if flight.departure_time + timedelta(hours=1) > flight.landing_time:
            self.logger.logger.error(f'{self.login_token} tried to update flight but the departure must to be at least '
                                     f'1 hour before landing time')
            raise LandingTimeBeforeDepartureTimeError(flight.landing_time, flight.departure_time)
        if flight.remaining_tickets < 50:
            raise RemainingTicketsError(flight.remaining_tickets)
        self.repo.update_by_id(Flight, Flight.id, current_flight.id, {Flight.origin_country_id: flight.origin_country_id
            , Flight.destination_country_id: flight.destination_country_id, Flight.departure_time: flight.departure_time
            , Flight.landing_time: flight.landing_time, Flight.remaining_tickets: flight.remaining_tickets})

    def add_flight(self, flight):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(f'{self.login_token} tried to use the function of airline company')
            raise WrongLoginTokenError(self.login_token.id)
        if not isinstance(flight, Flight):
            self.logger.logger.error(f'{self.login_token} tried to add flight but the flight {flight} is not a Flight '
                                     f'object.')
            raise WrongDataError
        if self.login_token.id != flight.airline_company_id:
            self.logger.logger.error(f'{self.login_token} tried to add flight that did not belong to the current '
                                     f'airline company')
            raise WrongLoginTokenError(self.login_token.id)
        if flight.destination_country_id == flight.origin_country_id:
            self.logger.logger.error(f'{self.login_token} tried to add flight but but the origin country and the '
                                     f'destination country are the same')
            raise OriginCountryAndDestinationCountryAreTheSameError(flight.origin_country_id,
                                                                    flight.destination_country_id)
        if not isinstance(flight.departure_time, datetime) or not isinstance(flight.landing_time, datetime):
            self.logger.logger.error(f'{self.login_token} tried to add flight but the departure time and the landing '
                                     f'time must be a datetime object.')
            raise WrongDataError
        if flight.departure_time + timedelta(hours=1) > flight.landing_time:
            self.logger.logger.error(f'{self.login_token} tried to add flight but the departure must to be at least 1 '
                                     f'hour before landing time')
            raise LandingTimeBeforeDepartureTimeError(flight.landing_time, flight.departure_time)
        if flight.remaining_tickets < 50:
            raise RemainingTicketsError(flight.remaining_tickets)
        self.repo.add(flight)

    def remove_flight(self, flight_id):
        if self.login_token.role != 'airline_companies':
            self.logger.logger.error(f'{self.login_token} tried to use the function of airline company')
            raise WrongLoginTokenError(self.login_token.id)
        if not isinstance(flight_id, int):
            self.logger.logger.error(f'{self.login_token} tried to remove flight but the flight_id is illegal')
            raise IllegalIdError
        flight = self.repo.get_by_id(Flight, flight_id)
        if flight is None:
            self.logger.logger.error(f'{self.login_token} tried to remove flight but the flight_id is not exist.')
            raise IdNotFoundError
        if self.login_token.id != flight.airline_company_id:
            self.logger.logger.error(f'{self.login_token} tried to remove flight that did not belong to the current '
                                     f'airline company')
            raise WrongLoginTokenError(self.login_token.id)
        self.repo.delete_by_id(Flight, Flight.id, flight_id)
