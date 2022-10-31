from Db_Config import local_session, create_all_entities
from Db_Repo import DbRepo
from facades.AirlineFacade import AirlineFacade
from LoginToken import *

repo = DbRepo(local_session)
create_all_entities()
repo.reset_test_db()

# airline = AirlineFacade(repo, LoginToken(1, 'ELAL', 'Airline'))
