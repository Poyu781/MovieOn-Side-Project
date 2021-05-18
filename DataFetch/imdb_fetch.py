import requests
import urllib.request
import ssl,os
import gzip
import dotenv
import datetime
from Modules.MySQL_module import SQL
today_date = datetime.datetime.today().date()
print(today_date)
# export PYTHONPATH="$PWD" 
dotenv.load_dotenv()
rds_host = os.getenv("rds_host")
rds_user = os.getenv("rds_user")
rds_password = os.getenv("rds_password")
movie_database = SQL(user=rds_user,password=rds_password,host=rds_host,database="movie")


# r = 1/0
class IMDb_fetch():
    ssl._create_default_https_context = ssl._create_unverified_context
    INSTALL_PATH = "DataSection/"
    def __init__(self,file_url,file_name):
        self.file_url = file_url
        self.file_name = file_name
    
    def install_data(self):
        print('Beginning file download with urllib2...')
        urllib.request.urlretrieve(self.file_url, self.INSTALL_PATH + self.file_name)
    
    def decompress_file(self):
        file_path = self.INSTALL_PATH + self.file_name
        with gzip.open(file_path) as f:
            file_content = f.read().decode("utf-8")
            data = file_content.split("\n")
            f.close()
        data.pop(0)
        data.pop(-1)
        return data

movie_rate = IMDb_fetch("https://datasets.imdbws.com/title.ratings.tsv.gz","movie_rate.tsv.gz")
# movie_rate.install_data()
rating_list = movie_rate.decompress_file()
print(len(rating_list))

def insert_rating(data):
    insert_rating_list = []
    for i in data :
        movie_rate_info = i.split("\t")
        movie_rate_info[1] = float(movie_rate_info[1])
        movie_rate_info[2] = int(movie_rate_info[2])
        movie_rate_info.append(today_date)
        # print(movie_rate_info)
        insert_rating_list.append(movie_rate_info)
    movie_database.bulk_execute("insert IGNORE into `IMDb_rating` (`IMDb_id`,`rating`,`rating_count`,`update_date`) values(%s, %s, %s, %s)",insert_rating_list)
    print("successful insert rating")


# movie_detail = IMDb_fetch("https://datasets.imdbws.com/title.basics.tsv.gz","movie_detail.tsv.gz")
# movie_detail.install_data()
# detail_list = movie_detail.decompress_file()
# print(len(detail_list))
def insert_detail(data):
    insert_detail_list = []
    for i in data :
        movie_detail_info = i.split("\t")
        try:
            if movie_detail_info[1] == "movie" and  movie_detail_info[5] != '\\N' and movie_detail_info[7] != '\\N' and int(movie_detail_info[5]) > 1980:
                movie_detail_info.pop(1)
                movie_detail_info.pop(5)
                movie_detail_info[4] = int(movie_detail_info[4])
                movie_detail_info[5] = int(movie_detail_info[5])
                insert_detail_list.append(movie_detail_info)
        except:
            print(movie_detail_info)
    movie_database.bulk_execute("INSERT INTO `movie_detail`(`IMDb_id`, `primary_title`, `original_title`, `is_adult`, `start_year`, `runtime_minutes`, `category`) VALUES (%s,%s,%s,%s,%s,%s,%s)",insert_detail_list)
# insert_rating(rating_list)
# # insert_detail(detail_list)
# print("si")
