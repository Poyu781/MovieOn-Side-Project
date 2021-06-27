import requests
import urllib.request
import ssl, os
import gzip
import dotenv
import datetime
from Modules.mysql_module import SQL
from Modules.mongo_db import movie_mongo_db
today_date = datetime.datetime.today().date()
print(today_date)
# export PYTHONPATH="$PWD"
dotenv.load_dotenv()
rds_host = os.getenv("rds_host")
rds_user = os.getenv("rds_user")
rds_password = os.getenv("rds_password")
movie_database = SQL(user=rds_user,
                     password=rds_password,
                     host=rds_host,
                     database="movie")

collection = movie_mongo_db.test
data = movie_mongo_db["data_"+"2021-06-24"]

# r = 1/0
class IMDb_fetch():
    ssl._create_default_https_context = ssl._create_unverified_context
    INSTALL_PATH = "DataSection/"

    def __init__(self, file_url, file_name):
        self.file_url = file_url
        self.file_name = file_name + str(today_date) + '.tsv.gz'

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


def insert_movie_detail_to_mongo(imdb_detail_data, start_year, end_year, feature_type):
    # get imdb_id from db
    existed_movie_list = []

    movie_detail_list = []
    imdb_id_list = []
    for i in imdb_detail_data:
        insert_dict = {}
        movie_detail_info = i.split("\t")
        try:
            if movie_detail_info[1] == feature_type and movie_detail_info[5] != '\\N' and movie_detail_info[7] != '\\N' and int(movie_detail_info[5]) >= start_year and int(movie_detail_info[5]) <= end_year:
                movie_detail_info.pop(1)  #remove type  (e.g. movie, short, tv series, tv episode, video, etc)
                movie_detail_info.pop(5)  #remove end_year (cause this is not series )
                movie_detail_info[4] = int(movie_detail_info[4])  # start_year
                movie_detail_info[5] = int(movie_detail_info[5])  # run_time
                insert_dict['imdb_id'] = movie_detail_info[0]
                insert_dict['primary_title'] = movie_detail_info[1]
                insert_dict['original_title'] = movie_detail_info[2]
                insert_dict['is_adult'] = movie_detail_info[3]
                insert_dict['start_year'] = movie_detail_info[4]
                insert_dict['runtime_minutes'] = movie_detail_info[5]
                insert_dict['category'] = movie_detail_info[6]
                movie_detail_list.append(insert_dict)
                imdb_id_list.append(movie_detail_info[0])
        except Exception as e:
            print(e)
            print(movie_detail_info)
    collection.insert_many(movie_detail_list)
    print("success insert into mongodb")
    return imdb_id_list


def insert_movie_rating_to_mysql(imdb_rating_data):
    insert_rating_list = []
    for i in imdb_rating_data:
        movie_rate_info = i.split("\t")
        movie_rate_info[1] = float(movie_rate_info[1])
        movie_rate_info[2] = int(movie_rate_info[2])
        movie_rate_info.append(today_date)
        # print(movie_rate_info)
        insert_rating_list.append(movie_rate_info)
    movie_database.bulk_execute(
        "insert IGNORE into `imdb_rating` (`IMDb_id`,`rating`,`rating_count`,`update_date`) values(%s, %s, %s, %s)", insert_rating_list)
    print("successful insert rating")


# movie_rate = IMDb_fetch("https://datasets.imdbws.com/title.ratings.tsv.gz","movie_rate")
# movie_rate.install_data()
# rating_list = movie_rate.decompress_file()
# print(len(rating_list))


def insert_rating(data):
    insert_rating_list = []
    for i in data:
        movie_rate_info = i.split("\t")
        movie_rate_info[1] = float(movie_rate_info[1])
        movie_rate_info[2] = int(movie_rate_info[2])
        movie_rate_info.append(today_date)
        # print(movie_rate_info)
        insert_rating_list.append(movie_rate_info)
    movie_database.bulk_execute(
        "insert IGNORE into `IMDb_rating` (`IMDb_id`,`rating`,`rating_count`,`update_date`) values(%s, %s, %s, %s)",
        insert_rating_list)
    print("successful insert rating")

if __name__ == "__main__":
    movie_detail = IMDb_fetch("https://datasets.imdbws.com/title.basics.tsv.gz","movie_detail")
    movie_detail.install_data()
    detail_list = movie_detail.decompress_file()
    print(len(detail_list))
# print(len(detail_list))
def insert_detail(data):
    insert_detail_list = []
    for i in data:
        movie_detail_info = i.split("\t")
        try:
            if movie_detail_info[1] == "movie" and movie_detail_info[
                    5] != '\\N' and movie_detail_info[7] != '\\N' and int(
                        movie_detail_info[5]) > 1980:
                movie_detail_info.pop(1)
                movie_detail_info.pop(5)
                movie_detail_info[4] = int(movie_detail_info[4])
                movie_detail_info[5] = int(movie_detail_info[5])
                insert_detail_list.append(movie_detail_info)
        except:
            print(movie_detail_info)
    movie_database.bulk_execute(
        "INSERT INTO `movie_detail`(`IMDb_id`, `primary_title`, `original_title`, `is_adult`, `start_year`, `runtime_minutes`, `category`) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        insert_detail_list)


# insert_rating(rating_list)
# # insert_detail(detail_list)
# print("si")
