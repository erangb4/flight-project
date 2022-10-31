from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker
from Logger import Logger
import pymongo


config = ConfigParser()
config.read("config.conf")

#SQL
connection_string = config["db"]["conn_string"]
Base = declarative_base()
engine = create_engine(connection_string, echo=True)

#MongoDB
cluster = pymongo.MongoClient(config["db"]["mongo_conn"])
db = cluster["airlock-userAuth"]
collection = db["users"]

logger = Logger.get_instance()
Session = sessionmaker()
local_session = Session(bind=engine)


def create_all_entities():
    try:
        Base.metadata.create_all(engine)
        logger.logger.debug('all the sql tables created.')
    except OperationalError:
        print('The database did not found, please check the connection string')
        logger.logger.critical('The database did not found, please check the connection string')

def mongo_insert(data):
    collection.insert_one(data)


def mongo_delete():
    collection.delete_many({})


def mongo_delete_one(username):
    collection.delete_one({'username': username})
