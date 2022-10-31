from tables.UserRole import UserRole
from facades.FacadeBase import FacadeBase
from exceptions.UsernameAlreadyExist import UsernameAlreadyExistError
from exceptions.PasswordTooShort import PasswordTooShortError
from facades.AirlineFacade import AirlineFacade
from facades.AdministratorFacade import AdministratorFacade
from facades.CustomerFacade import CustomerFacade
from tables.User import User
from tables.Customer import Customer
from exceptions.WrongData import WrongDataError
from exceptions.WrongEmail import WrongEmailError
from tables.AirlineCompany import AirlineCompany
from tables.Administrator import Administrator
from LoginToken import LoginToken
from exceptions.WrongUser import WrongUserError


class AnonymousFacade(FacadeBase):

    def __init__(self, repo):
        self.repo = repo
        super().__init__(self.repo)

    def login(self, username, password):
        user = self.repo.get_user(username, password)[0]
        if not user:
            self.logger.logger.info(f'wrong user: {username} or password: {password}')
            raise WrongUserError(username)
        else:
            if user.user_role == 3:
                admin = self.repo.get_admin_by_something(Administrator.user_id, user.id)[0]
                role_name = self.repo.get_user_role_by_id(user.user_role)
                return AdministratorFacade(self.repo, LoginToken.LoginToken(admin.id, admin.first_name, role_name))
            elif user.user_role == 2:
                airline = self.repo.get_airlines_by_something(AirlineCompany.user_id, user.id)[0]
                role_name = self.repo.get_user_role_by_id(user.user_role)
                return AirlineFacade(self.repo, LoginToken.LoginToken(airline.id, airline.name, role_name))
            elif user.user_role == 3:
                customer = self.repo.get_customers_by_something(Customer.user_id, user.id)[0]
                role_name = self.repo.get_user_role_by_id(user.user_role)
                return CustomerFacade(self.repo, LoginToken.LoginToken(customer.id, customer.name, role_name))
            else:
                return

    def create_user(self, user):
        if not isinstance(user, User):
            self.logger.logger.error(f'{self.login_token} tried to create user but the user is not a User instance.')
            raise WrongDataError
        if self.repo.get_user(user.username, user.password) is not None:
            self.logger.logger.error(f'{self.login_token} tried to create user but the user is already exist.')
            raise UsernameAlreadyExistError(user.username)
        if user.password.range < 6:
            self.logger.logger.error(f'{self.login_token} tried to create user but the password is too short.')
            raise PasswordTooShortError()
        if self.repo.get_by_condition(User, lambda query: query.filter(User.email == user.email).all()) is not None:
            self.logger.logger.error(f'{self.login_token} tried to create user but the email is already exist.')
            raise WrongEmailError(user.email)
        if user.user_role != 1 or user.user_role != 2 or user.user_role != 3:
            self.logger.logger.error(f'{self.login_token} tried to create user but the user_role is illegal.')
            raise WrongDataError
        self.repo.add(user)

    def add_customer(self, customer):
        if not isinstance(customer, Customer):
            self.logger.logger.error(f'{self.login_token} tried to add customer but the customer: "{customer}" is '
                                     f'not a Customer object.')
            raise WrongDataError
        if self.repo.get_customers_by_something(Customer.phone_no, customer.phone_no):
            self.logger.logger.error(f'{self.login_token} tried to add customer but the phone number is already exist.')
            raise WrongDataError
        if self.repo.get_customers_by_something(Customer.credit_card_no, customer.credit_card_no):
            self.logger.logger.error(f'{self.login_token} tried to add customer but the credit card number is already '
                                     f'already exist')
            raise WrongDataError
        self.repo.add(customer)
