from project.facades.AnonymousFacade import *
from project.classes.Customer import Customer
from project.classes.Flight import Flight
from project.classes.Ticket import Ticket
from project.exceptions.NoMoreTickets import NoMoreTicketsError
from project.exceptions.WrongLoginToken import WrongLoginTokenError


class CustomerFacade(FacadeBase):

    def __init__(self, repo, login_token):
        self.repo = repo
        super().__init__(repo)
        self._login_token = login_token()

    def update_customer(self, customer):
        if self.login_token.role != 'customers':
            self.logger.logger.error(f'{self.login_token} tried to use the function of customers')
            raise WrongLoginTokenError(self.login_token.id)
        if not isinstance(customer, Customer):
            self.logger.logger.error(f'{self.login_token} tried to update customer but the customer: "{customer}" is '
                                     f'not a Customer object.')
            raise WrongDataError
        current_customer = self.repo.get_by_id(Customer, self.login_token)
        if not current_customer:
            self.logger.logger.error(f'{self.login_token} tried to update customer but the customer did not found')
            raise WrongDataError
        if self.repo.get_customers_by_something(Customer.phone_no, customer.phone_no) and \
                self.repo.get_customers_by_something(Customer.phone_no, customer.phone_no) != current_customer:
            self.logger.logger.error(f'{self.login_token} tried to update customer but the phone number is already '
                                     f'exist')
            raise WrongDataError
        if self.repo.get_customers_by_something(Customer.credit_card_no, customer.credit_card_no) and \
                self.repo.get_customers_by_something(Customer.credit_card_no, customer.credit_card_no) != \
                current_customer:
            self.logger.logger.error(f'{self.login_token} tried to update customer but the credit card number is '
                                     f'already exist')
            raise WrongDataError
        self.repo.update_by_id(Customer, Customer.id, self.login_token.id,
                               {Customer.first_name: customer.first_name, Customer.last_name: customer.last_name,
                                Customer.address: customer.address, Customer.phone_no: customer.phone_no,
                                Customer.credit_card_no: customer.credit_card_no})

    def add_ticket(self, ticket):
        if self.login_token.role != 'customers':
            self.logger.logger.error(f'{self.login_token} tried to use the function of customers')
            raise WrongLoginTokenError(self.login_token.id)
        if not isinstance(ticket, Ticket):
            self.logger.logger.error(f'{self.login_token} tried to add ticket but the ticket: "{ticket}" is not a '
                                     f'Ticket object.')
            raise WrongDataError
        flight = self.repo.get_by_id(Flight, ticket.flight_id)
        if not flight:
            self.logger.logger.error(f'{self.login_token} tried to add ticket but the flight did not found')
            raise WrongDataError
        if self.repo.get_remaining_tickets(ticket) < 1:
            self.logger.logger.error(f'{self.login_token} tried to add ticket but the flight is full')
            raise NoMoreTicketsError(ticket.flight_id)
        if self.repo.get_tickets_by_customer_id(self.login_token.id):
            self.logger.logger.error(f'{self.login_token} tried to add ticket but he already has a ticket for this '
                                     f'flight')
            raise NoMoreTicketsError(ticket.flight_id)
        self.repo.add(ticket)
        self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,
                               {Flight.remaining_tickets: Flight[0].remaining_tickets - 1})

    def remove_ticket(self, ticket):
        if self.login_token.role != 'customers':
            self.logger.logger.error(f'{self.login_token} tried to use the function of customers')
            raise WrongLoginTokenError(self.login_token.id)
        if not isinstance(ticket, Ticket):
            self.logger.logger.error(f'{self.login_token} tried to remove ticket but the ticket: "{ticket}" is not a '
                                     f'Ticket object.')
            raise WrongDataError
        ticket = self.repo.get_by_id(Ticket, ticket.id)
        if not ticket:
            self.logger.logger.error(f'{self.login_token} tried to remove ticket but the ticket did not found')
            raise WrongDataError
        if self.login_token.id != ticket.customer_id:
            self.logger.logger.error(f'{self.login_token} tried to remove ticket but the ticket not belong to him')
            raise WrongLoginTokenError(self.login_token.id)
        self.repo.delete_by_id(Ticket, Ticket.id, ticket.id)
        self.repo.update_by_id(Flight, Flight.id, ticket.flight_id,
                               {Flight.remaining_tickets: Flight.remaining_tickets + 1})

    def get_tickets_by_customer(self):
        if self.login_token.role != 'customers':
            self.logger.logger.error(f'{self.login_token} tried to use the function of customers')
            raise WrongLoginTokenError(self.login_token.id)
        return self.repo.get_tickets_by_customer_id(self.login_token.id)
