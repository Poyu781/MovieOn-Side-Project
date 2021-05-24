import dotenv,os
dotenv.load_dotenv()
mongo_server = os.getenv("mongo_server")
mongo_user = os.getenv("mongo_user")
mongo_password = os.getenv("mongo_password")

rds_host = os.getenv("rds_host")
rds_user = os.getenv("rds_user")
rds_password = os.getenv("rds_password")
secret_key = os.getenv("SECRET_KEY")