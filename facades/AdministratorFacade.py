from project.facades.AnonymousFacade import *
from project.classes.AirlineCompany import AirlineCompany
from project.classes.Administrator import Administrator
from project.classes.Country import Country
from project.classes.Customer import Customer
from project.classes.User import User
from project.exceptions.NameAlreadyExist import NameAlreadyExistError
from project.exceptions.UserAlreadyExist import UserAlreadyExistError
from project.exceptions.PhoneNumberAlreadyExist import PhoneNumberAlreadyExistError
from project.exceptions.CreditCardAlredyExist import CreditCardAlreadyExistError
from project.exceptions.WrongLoginToken import WrongLoginTokenError
from project.exceptions.IdNotFound import IdNotFoundError


class AdministratorFacade(FacadeBase):

    def __init__(self, repo, login_token):
        self.repo = repo
        super().__init__(self.repo)
        self._login_token = login_token

    def get_all_customers(self):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        else:
            return self.repo.get_all(Customer)

    def get_all_airlines(self):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        else:
            return self.repo.get_all(AirlineCompany)

    def get_all_administrators(self):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        else:
            return self.repo.get_all(Administrator)

    def add_airline(self, airline):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        if self.repo.get_airline_by_something(AirlineCompany.name, airline.name) is not None:
            self.logger.logger.error(f'{self.login_token} tried to add airline with name that already exist.')
            raise NameAlreadyExistError(airline.name)
        if self.repo.get_by_id(Country, airline.country_id) is None:
            self.logger.logger.error(f'{self.login_token} tried to add airline with country_id that not exist.')
            raise IdNotFoundError(airline.country_id)
        if self.repo.get_admin_by_something(Administrator.user_id, airline.user_id) is not None or \
                self.repo.get_customer_by_something(Customer.user_id, airline.user_id) is not None or \
                self.repo.get_airline_by_something(AirlineCompany.user_id, airline.user_id) is not None:
            self.logger.logger.error(f'{self.login_token} tried to add airline with user_id that already exist.')
            raise UserAlreadyExistError(airline.user_id)
        self.repo.add(airline)

    def add_customer(self, customer):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        if self.repo.get_customer_by_something(Customer.phone_no, customer.phone_no) is not None:
            self.logger.logger.error(f'{self.login_token} tried to add customer with phone_no that already exist.')
            raise PhoneNumberAlreadyExistError(customer.phone_no)
        if self.repo.get_customer_by_something(Customer.credit_card_no, customer.credit_card_no) is not None:
            self.logger.logger.error(f'{self.login_token} tried to add customer with credit_card_no that already exist.')
            raise CreditCardAlreadyExistError(customer.credit_card_no)
        if self.repo.get_admin_by_something(Administrator.user_id, customer.user_id) is not None or \
                self.repo.get_customer_by_something(Customer.user_id, customer.user_id) is not None or \
                self.repo.get_airline_by_something(AirlineCompany.user_id, customer.user_id) is not None:
            self.logger.logger.error(f'{self.login_token} tried to add customer with user_id that already exist.')
            raise UserAlreadyExistError(customer.user_id)
        self.repo.add(customer)

    def add_administrator(self, admin):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        if self.repo.get_admin_by_something(Administrator.user_id, admin.user_id) is not None or \
                self.repo.get_customer_by_something(Customer.user_id, admin.user_id) is not None or \
                self.repo.get_airline_by_something(AirlineCompany.user_id, admin.user_id) is not None:
            self.logger.logger.error(f'{self.login_token} tried to add admin with user_id that already exist.')
            raise UserAlreadyExistError(admin.user_id)
        self.repo.add(admin)

    def remove_airline(self, airline):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        if self.repo.get_by_id(AirlineCompany, airline.id) is None:
            self.logger.logger.error(f'{self.login_token} tried to remove airline that not exist')
            raise IdNotFoundError(airline.id)
        self.repo.delete_by_id(AirlineCompany, AirlineCompany.id, airline.id)

    def remove_customer(self, customer):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        if self.repo.get_by_id(AirlineCompany, customer.id) is None:
            self.logger.logger.error(f'{self.login_token} tried to remove customer that not exist')
            raise IdNotFoundError(customer.id)
        self.repo.delete_by_id(Customer, Customer.id, customer.id)

    def remove_user(self, user):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        if self.repo.get_by_id(AirlineCompany, user.id) is None:
            self.logger.logger.error(f'{self.login_token} tried to remove user that not exist')
            raise IdNotFoundError(user.id)
        self.repo.delete_by_id(User, User.id, user.id)

    def remove_administrator(self, admin):
        if self.login_token.role != 'administrator':
            self.logger.logger.error(f'{self.login_token} tried to use the function of administrator')
            raise WrongLoginTokenError
        if self.repo.get_by_id(AirlineCompany, admin.id) is None:
            self.logger.logger.error(f'{self.login_token} tried to remove admin that not exist')
            raise IdNotFoundError(admin.id)
        self.repo.delete_by_id(Administrator, Administrator.id, admin.id)
