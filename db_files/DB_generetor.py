import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, StringProperty
from DbDataObject import DbDataObject
from exceptions.DbGenDataNotValidError import DbGenDataNotValidError
from RabbitProducerObject import RabbitProducerObject
from RabbitConsumerObject import RabbitConsumerObject
import json
from Db_Config import local_session
from Db_Repo import DbRepo
from threading import Thread


class DbGenWidget(Widget):
    airline_companies = ObjectProperty(None)
    customers = ObjectProperty(None)
    flights_per_company = ObjectProperty(None)
    tickets_per_customer = ObjectProperty(None)
    my_progress_bar = ObjectProperty(None)
    alerts_label = StringProperty('')
    repo = DbRepo(local_session)
    rabbit_producer = RabbitProducerObject('DataToGenerate')
    already_generated = False

    def update_progress_bar(self, value):
        self.ids.my_progress_bar.value = value

    # root.btn() in kv file
    def btn(self):
        if self.already_generated:
            self.ids.alerts_label.text = 'The data was already generated, please close the app.'
            return
        try:
            airlines = self.airline_companies.text
            customers = self.customers.text
            flights_per_company = self.flights_per_company.text
            tickets_per_customer = self.tickets_per_customer.text
            db_data_object = DbDataObject(customers=customers, airlines=airlines,
                                          flights_per_airline=flights_per_company,
                                          tickets_per_customer=tickets_per_customer)
            db_data_object.validate_data()
            self.rabbit_producer.publish(json.dumps(db_data_object.__dict__()))
            self.already_generated = True
            self.ids.alerts_label.text = 'Generating Data...'

        except DbGenDataNotValidError:
            self.ids.alerts_label.text = 'Data is not Valid!'


Builder.load_file('my1.kv')

dbgen = DbGenWidget()


def get_db_gen():
    return dbgen


class MyApp(App):
    def build(self):
        return get_db_gen()


def callback(ch, method, properties, body):
    data = json.loads(body)
    progress_bar_value = list(data.values())[0]
    kivy_app = get_db_gen()
    kivy_app.ids.alerts_label.text = f'Generating {list(data.keys())[0]}'
    kivy_app.update_progress_bar(progress_bar_value) # updating the progress bar
    if progress_bar_value == 100:
        kivy_app.ids.alerts_label.text = 'The data was successfully generated!'


if __name__ == "__main__":

    repo = DbRepo(local_session)
    repo_thread = Thread(target=repo.reset_all_tables_auto_inc)
    repo_thread.start()
    rabbit_consumer = RabbitConsumerObject(q_name='GeneratedData', callback=callback)
    t1 = Thread(target=rabbit_consumer.consume)
    t1.setDaemon(True)
    t1.start()
    MyApp().run()
