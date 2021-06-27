from pymongo import MongoClient
# from config import mongo_password,mongo_server,mongo_user
class ConnectMongo():
    def __init__(self,host,username,password,database,authMechanism='SCRAM-SHA-1'):
        self.connect_kwargs = {
            'username' : username,
            'password' : password,
            'authSource' : database,
            'authMechanism' : authMechanism,
        }
        self.host = host
        self.db_name = database
    def db_init(self):
        connect = MongoClient(self.host,**self.connect_kwargs)
        db = connect[self.db_name]
        return db

movie_db = ConnectMongo(host="127.0.0.1:27017",username='poyu2',password='root',database="movie")
movie_mongo_db = movie_db.db_init()



