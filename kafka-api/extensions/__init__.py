from .settions import mongo_db
from .mongoApi import MongoConn


MonConn = MongoConn(log=False, db=mongo_db)
