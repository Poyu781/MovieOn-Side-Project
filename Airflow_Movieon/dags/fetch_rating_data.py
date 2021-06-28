import sys
import time
import re
import os,json
from pprint import pprint
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import defaultdict

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator

from modules.mysql_module import SQL
from modules.imdb_fetch import IMDb_fetch,BASE_DIR,movie_mongo_db
from modules import mail_notification
from modules import crawl


default_args = {
    'owner': 'Poyu',
    'start_date': datetime(2021, 6, 26, 0, 0),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

today_date = datetime.today().date()
from config import rds_host,rds_password,rds_user
movie_new_db =  SQL(user=rds_user,password=rds_password,host=rds_host,database="movie_new")

fetch_id_relation = movie_new_db.fetch_list("select id,douban_id,imdb_id,rotten_tomato_id from movie_new.webs_id_relation where douban_id != 'Null'")
id_relation_dict = {}
for data in fetch_id_relation :
    id_relation_dict[data[1]]=data[0]
    id_relation_dict[data[2]]=data[0]
    try:
        id_relation_dict[data[3]]=data[0]
    except:
        continue

def insert_imdb_rating():
    imdb_id_list = [i[0] for i in movie_new_db.fetch_list("select imdb_id from movie_new.webs_id_relation where douban_id != 'Null'")]
    imdb_movie_rating_data = IMDb_fetch("https://datasets.imdbws.com/title.ratings.tsv.gz","movie_rating",today_date)
    imdb_movie_rating_data.install_data()
    data = imdb_movie_rating_data.decompress_file()
    insert_rating_list = []
    for i in data:
        movie_rate_info = i.split("\t")
        imdb_id = movie_rate_info[0]
        try:
            movie_rate_info[0] = id_relation_dict[imdb_id]
            movie_rate_info[1] = float(movie_rate_info[1])
            movie_rate_info[2] = int(movie_rate_info[2])
            movie_rate_info.append(today_date)
            # print(movie_rate_info)
            insert_rating_list.append(movie_rate_info)
        except:
            continue
    movie_new_db.bulk_execute("insert into `imdb_rating` (`internal_id`,`rating`,`rating_count`,`update_date`) values(%s, %s, %s, %s)", insert_rating_list)

def insert_douban_rating():
    douban_id_list = [i[0] for i in movie_new_db.fetch_list("select douban_id from movie_new.webs_id_relation where douban_id != 'Null'")]
    error_file_path = os.path.join(BASE_DIR, 'data/error_json/douban_rating_error_log.json')
    douban_rating_error_log = open(error_file_path,"a")
    insert_data = []
    failed_list = []
    
    def fetch_douban_rating(fixed_url, search_id,error_file):
        try:
            single_douban_data =[]
            soup = crawl.fetch_data(fixed_url, search_id)        
            internal_id = id_relation_dict[search_id]
            single_douban_data.append(internal_id)
            avg_rating = soup.find("strong",property="v:average").text
            rating_amount = soup.find("span",property="v:votes").text
            single_douban_data.append(avg_rating)
            rating_ratio_list =soup.find("div",class_="ratings-on-weight").find_all("span",class_= "rating_per")
            for ratio in rating_ratio_list :
                single_douban_data.append(ratio.text[:-1])
            single_douban_data.append(rating_amount)
            single_douban_data.append(today_date)
            insert_data.append(single_douban_data)
            print(f"success {internal_id} douban: {search_id}")
        except Exception as e:
            failed_list.append(search_id)
            error_file.write(json.dumps({'douban_id':search_id, "internal_id":internal_id, "error_msg":str(e)})+'\n')
    crawl.main(fetch_douban_rating,"https://movie.douban.com/subject/",douban_id_list[12000:],douban_rating_error_log)
    for i in range(2,5):
        if failed_list != []:
            retry_list = failed_list
            failed_list = []
            douban_rating_error_log.write(f"________failed {i}nd line______\n")
            crawl.main(fetch_douban_rating,"https://movie.douban.com/subject/",retry_list,douban_rating_error_log)
    douban_rating_error_log.close()
    movie_new_db.bulk_execute('''INSERT INTO `douban_rating`( `internal_id`, `avg_rating`, `five_star_ratio`,
     `four_star_ratio`, `three_star_ratio`, `two_star_ratio`, `one_star_ratio`, 
     `total_rating_amount`, `update_date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',insert_data)


def insert_tomato_rating():
    tomato_id_list = [i[0] for i in movie_new_db.fetch_list("select rotten_tomato_id from movie_new.webs_id_relation where rotten_tomato_id != 'Null'")]
    error_file_path = os.path.join(BASE_DIR, 'data/error_json/tomato_rating_error_log.json')
    tomato_rating_error_log = open(error_file_path,"a")
    insert_data = []
    failed_list = []
    def fetch_tomato_rating(fixed_url, search_id,error_file):
        try:
            soup = crawl.fetch_data(fixed_url, search_id)
            internal_id = id_relation_dict[search_id]

            reviews = soup.find("script", id = "score-details-json").string
            reviews_dict =json.loads(reviews)
            tomator_rating = reviews_dict["scoreboard"]['tomatometerScore']
            tomator_count = reviews_dict["scoreboard"]['tomatometerCount']
            audience_rating = reviews_dict["scoreboard"]['audienceScore']
            audience_count = reviews_dict["scoreboard"]['audienceCount']
            insert_data.append([internal_id,audience_rating,audience_count,tomator_rating,tomator_count,today_date])
            print(f"success {internal_id} tomato: {search_id}")
        except Exception as e:
            failed_list.append(search_id)
            error_file.write(json.dumps({'tomato_id':search_id, "internal_id":internal_id, "error_msg":str(e)})+'\n')
    crawl.main(fetch_tomato_rating,"https://www.rottentomatoes.com/m/",tomato_id_list,tomato_rating_error_log)
    for i in range(2,5):
        if failed_list != []:
            retry_list = failed_list
            failed_list = []
            tomato_rating_error_log.write(f"________failed {i}nd line______\n")
            crawl.main(fetch_tomato_rating,"https://www.rottentomatoes.com/m/",retry_list,tomato_rating_error_log)
    tomato_rating_error_log.close()
    movie_new_db.bulk_execute("INSERT INTO `rotten_tomato_rating`(`internal_id`, `audience_rating`, `audience_rating_amount`, `tomator_rating`, `tomator_rating_amount`, `update_date`) VALUES (%s,%s,%s,%s,%s,%s)",insert_data)

def calculate_rating_standard_deviation_and_mean():
    pass

with DAG('fetch_insert_rating_data', default_args=default_args) as dag:

    insert_imdb_rating = PythonOperator(
        task_id = "insert_imdb_rating",
        python_callable = insert_imdb_rating
    )

    insert_douban_rating = PythonOperator(
        task_id = "insert_douban_rating",
        python_callable = insert_douban_rating
    )

    insert_tomato_rating = PythonOperator(
        task_id = "insert_tomato_rating",
        python_callable = insert_tomato_rating
    )

    calculate_rating_standard_deviation_and_mean = PythonOperator(
        task_id = "calculate_rating_standard_deviation_and_mean",
        python_callable = calculate_rating_standard_deviation_and_mean
    )
    [insert_imdb_rating,insert_douban_rating,insert_tomato_rating] >> calculate_rating_standard_deviation_and_mean
    #  >> calculate_rating_standard_deviation_and_mean
    #  >> calculate_rating_standard_deviation_and_mean
