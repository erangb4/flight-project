from datetime import datetime
from Logger import Logger
from tables.Country import Country
from tables.AirlineCompany import AirlineCompany
from tables.Customer import Customer
from tables.Flight import Flight
from tables.Ticket import Ticket
from tables.User import User
from tables.UserRole import UserRole
from tables.Administrator import Administrator
from sqlalchemy.exc import OperationalError


class DbRepo:

    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = Logger.get_instance()

    def reset_auto_inc(self, table_class):
        try:
            self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')
            self.local_session.commit()
            self.logger.logger.debug(f'Reset auto inc in {table_class} table')
        except OperationalError as a:
            self.logger.logger.critical(a)

    def add(self, one_row):
        try:
            self.local_session.add(one_row)
            self.local_session.commit()
            self.logger.logger.debug(f'{one_row} added to the DB.')
        except OperationalError as a:
            self.logger.logger.critical(a)

    def add_all(self, rows_list):
        try:
            self.local_session.add(rows_list)
            self.local_session.commit()
            self.logger.logger.debug(f'{rows_list} added to the DB.')
        except OperationalError as a:
            self.logger.logger.critical(a)

    def delete_by_id(self, table_class, id_column_name, id):
        try:
            self.local_session.query(table_class).filter(id_column_name == id).delete(synchronize_session=False)
            self.local_session.commit()
            self.logger.logger.debug(f'{id} deleted from {table_class}')
        except OperationalError as a:
            self.logger.logger.critical(a)

    def update_by_id(self, table_class, id_column_name, _id, data):
        try:
            self.local_session.query(table_class).filter(id_column_name == _id).update(data)
            self.local_session.commit()
            self.logger.logger.debug(f'{_id} has been updated from {table_class}: {data}.')
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_all(self, table_class):
        try:
            return self.local_session.query(table_class).all()
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_by_id(self, table_class, id):
        try:
            return self.local_session.query(table_class).get(id)
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_user(self, username, password):
        try:
            return self.local_session.query(User).filter(User.username == username and User.password == password).all()
        except OperationalError as a:
            self.logger.logger.critical(a)

    def check_user(self, username):
        try:
            if self.local_session.query(User).filter(User.username == username).all is not None:
                return True
            else:
                return False
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_flights_by_something(self, id_column_name, id):
        try:
            return self.local_session.query(Flight).filter(id_column_name == id).all()
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_customers_by_something(self, id_column_name, id):
        try:
            return self.local_session.query(Customer).filter(id_column_name == id).all()
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_airlines_by_something(self, id_column_name, id):
        try:
            return self.local_session.query(Customer).filter(id_column_name == id).all()
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_admin_by_something(self, id_column_name, id):
        try:
            return self.local_session.query(Administrator).filter(id_column_name == id).all()
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_tickets_by_customer_id(self, customer_id):
        try:
            return self.local_session.query(Ticket).filter(Ticket.customer_id == customer_id).all()
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_by_condition(self, table_class, cond):
        try:
            query_result = self.local_session.query(table_class)
            result = cond(query_result)
            return result
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_remaining_tickets(self, ticket):
        try:
            flight = self.local_session.query(Flight).get(ticket.flight_id)
            return flight.remaining_tickets
        except OperationalError as a:
            self.logger.logger.critical(a)

    def get_user_role_by_id(self, id):
        try:
            user_role = self.local_session.query(UserRole).get(id)
            return user_role
        except OperationalError as a:
            self.logger.logger.critical(a)

    def create_all_sp(self, file):
        try:
            try:
                with open(file, 'r') as sp_file:
                    queries = sp_file.read().split('|||')
                for query in queries:
                    self.local_session.execute(query)
                self.local_session.commit()
                self.logger.logger.debug(f'all sp from {file} were created.')
            except FileNotFoundError:
                self.logger.logger.critical(f'Tried to create all sp from the the file "{file}" but file was not found')
        except OperationalError as e:
            self.logger.logger.critical(e)

    def drop_all_tables(self):
        try:
            self.local_session.execute('DROP TABLE users CASCADE')
            self.local_session.execute('DROP TABLE user_roles CASCADE')
            self.local_session.execute('DROP TABLE tickets CASCADE')
            self.local_session.execute('DROP TABLE flights CASCADE')
            self.local_session.execute('DROP TABLE customers CASCADE')
            self.local_session.execute('DROP TABLE countries CASCADE')
            self.local_session.execute('DROP TABLE airline_companies CASCADE')
            self.local_session.execute('DROP TABLE administrators CASCADE')
            self.local_session.commit()
            self.logger.logger.debug(f'All tables Dropped.')
        except OperationalError as a:
            self.logger.logger.critical(a)

    def reset_all_tables_auto_inc(self):
        try:
            # resetting auto increment for all tables
            self.reset_auto_inc(Country)
            self.reset_auto_inc(UserRole)
            self.reset_auto_inc(User)
            self.reset_auto_inc(Administrator)
            self.reset_auto_inc(AirlineCompany)
            self.reset_auto_inc(Customer)
            self.reset_auto_inc(Flight)
            self.reset_auto_inc(Ticket)
        except OperationalError as e:
            self.logger.logger.critical(e)

    def reset_test_db(self):
        try:
            # resetting the auto increment for all the tables
            self.reset_auto_inc(Country)
            self.reset_auto_inc(UserRole)
            self.reset_auto_inc(User)
            self.reset_auto_inc(Administrator)
            self.reset_auto_inc(AirlineCompany)
            self.reset_auto_inc(Customer)
            self.reset_auto_inc(Flight)
            self.reset_auto_inc(Ticket)
            # county
            self.add(Country(name='Israel'))
            self.add(Country(name='Usa'))
            # user role
            self.add(UserRole(role_name='Customer'))
            self.add(UserRole(role_name='Airline Company'))
            self.add(UserRole(role_name='Administrator'))
            self.add(UserRole(role_name='Anonymous'))
            # user
            self.add(User(username='bibi', password='1234567', email='bibi@gmail.com', user_role=1))
            self.add(User(username='benet', password='1234567', email='benet@gmail.com', user_role=1))
            self.add(User(username='miri', password='1234567', email='miri@gmail.com', user_role=2))
            self.add(User(username='gidi', password='1234567', email='gidi@gmail.com', user_role=2))
            self.add(User(username='itay', password='1234567', email='itay@gmail.com', user_role=3))
            self.add(User(username='yochi', password='1234567', email='yochi@gmail.com', user_role=3))
            self.add(User(username='babi', password='1234567', email='babii@gmail.com', user_role=3))
            # administrator
            self.add(Administrator(first_name='itay', last_name='rab', user_id=5))
            self.add(Administrator(first_name='yochi', last_name='yoch', user_id=6))
            # airline company
            self.add(AirlineCompany(name='miri', country_id=1, user_id=3))
            self.add(AirlineCompany(name='gidi', country_id=2, user_id=4))
            # customer
            self.add(Customer(first_name='bibi', last_name='natan', address='herzel 4',
                              phone_no='0544444444', credit_card_no='0000', user_id=1))
            self.add(Customer(first_name='benet', last_name='nftul', address='mor 7',
                              phone_no='0522222222', credit_card_no='0001', user_id=2))
            # flight
            self.add(Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                            departure_time=datetime(2022, 3, 15, 6, 0, 0),
                            landing_time=datetime(2022, 3, 15, 10, 0, 0), remaining_tickets=200))
            self.add(Flight(airline_company_id=2, origin_country_id=1, destination_country_id=2,
                            departure_time=datetime(2022, 2, 20, 6, 0, 0),
                            landing_time=datetime(2022, 2, 20, 10, 0, 0), remaining_tickets=0))
            # ticket
            self.add(Ticket(flight_id=1, customer_id=1))
            self.add(Ticket(flight_id=2, customer_id=2))
            self.logger.logger.debug(f'Reset flights_db_tests')
        except OperationalError as a:
            self.logger.logger.critical(a)
