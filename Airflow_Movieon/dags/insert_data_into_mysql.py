import sys
import time
import re
import os,json
import urllib
from pprint import pprint
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import defaultdict
from difflib import SequenceMatcher
from opencc import OpenCC

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator

from modules import mail_notification
from modules import crawl
from modules.mysql_module import SQL
from modules.imdb_fetch import IMDb_fetch,BASE_DIR,movie_mongo_db


default_args = {
    'owner': 'Poyu',
    'start_date': datetime(2021, 6, 26, 0, 0),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

cc = OpenCC('s2twp')
today_date = datetime.today().date()
collection = movie_mongo_db["data_"+str(today_date)]
feature_dict = {'Comedy': 1, 'Fantasy': 2, 'Romance': 3, 'Drama': 4,'Action': 5,'Thriller': 6,'War': 7,'Adventure': 8,'Animation': 9,'Family': 10,'Mystery': 11,'Horror': 12,
'Sci-Fi': 13,'Crime': 14,'Biography': 15,'History': 16,'Music': 17,'Sport': 18,'Western': 19,'Musical': 20,'Documentary': 21,'Adult': 22,'News': 24}
from config import rds_host,rds_password,rds_user
movie_new_db =  SQL(user=rds_user,password=rds_password,host=rds_host,database="movie_new")
id_data = collection.find({"douban_id":{'$ne': None}})
def insert_web_id_relation():
    lastest_id = movie_new_db.fetch_list("select id from webs_id_relation order by id desc limit 1")[0][0]
    insert_list = []
    imdb_id_list = []
    for i in id_data :
        lastest_id += 1
        try :
            tomato_id =  i['rotten_tomato_id']
        except: 
            tomato_id = None
        insert_list.append([lastest_id,i['imdb_id'],i['douban_id'],tomato_id])
        collection.update_one( { "douban_id" : i['douban_id'] },{ "$set" : { 'internal_id' :lastest_id} } , upsert=True)
    print(insert_list)
    try :
        movie_new_db.bulk_execute("INSERT INTO `webs_id_relation`(`id`,`imdb_id`, `douban_id`, `rotten_tomato_id`) VALUES (%s,%s,%s,%s)",insert_list)
        return True,"success",insert_list
    except Exception as e:
        print(e)
        # send email ?
        return False,str(e),insert_list

def check_new_data_insert_status(**context):
    insert_success,error_msg,insert_list = context['task_instance'].xcom_pull(task_ids='insert_web_id_relation')
    if insert_success  :
        return 'insert_movie_basic_info'
    else:
        return 'alert_error_insert'
def alert_error_insert(**context):
    insert_success,error_msg,insert_list = context['task_instance'].xcom_pull(task_ids='insert_web_id_relation')
    print(error_msg)
    print(insert_list)
def insert_movie_basic_info():
    insert_movies_basic_info_list = []
    insert_other_movie_titles_list = []
    insert_description_list = []
    for i in id_data :
        desc = i['douban_description']
        if desc != None :
            desc = desc.replace(u'\u3000',u'').replace("\n","")
        else:
            desc = ""
        find_taiwan_name = False
        movie_names_list = []
        movie_names_list.extend(i['douban_movie_title'].split(" ", 1))
        if i['douban_movie_other_names'] != [] :
            movie_names_list.extend(i['douban_movie_other_names'].split(" / "))
        if  i['original_title'] not in movie_names_list:
            movie_names_list.append(i['original_title'])
        if i['primary_title'] not in movie_names_list:
            movie_names_list.append(i['primary_title'])
        for index in range(len(movie_names_list)) :
            movie_names_list[index] = cc.convert(movie_names_list[index])
            movie_name = movie_names_list[index]
            if  "(臺" in movie_name or "臺)" in movie_name:
                split_index = movie_name.index("(")
                chinese_name = movie_name[:split_index]
                find_taiwan_name = True
            if "港)" in movie_name or "(港" in movie_name or "(臺" in movie_name or "臺)" in movie_name :
                split_index = movie_name.index("(")
                movie_names_list[index] = movie_name[:split_index]
        if not find_taiwan_name : 
            chinese_name = movie_names_list[0]
        movie_other_name_insert_list = []
        for name in movie_names_list :
            movie_other_name_insert_list.append([name,i['internal_id']])
        insert_movies_basic_info_list.append([i['internal_id'],chinese_name,i['primary_title'],i['is_adult'],i['start_year'],i['douban_published_date'],cc.convert(i['douban_movie_country']),i['runtime_minutes'],i['douban_image']])
        insert_other_movie_titles_list.extend(movie_other_name_insert_list)
        insert_description_list.append([i['internal_id'],cc.convert(desc)])
    movie_new_db.bulk_execute('''INSERT INTO `movie_basic_info`
    (`internal_id`, `main_taiwan_name`, `main_original_name`, `is_adult`, `start_year`,
    `date_in_theater`, `publish_country`, `runtime_minutes`, `img`) VALUES (%s, %s, %s, %s, %s, %s ,%s, %s, %s)''',insert_movies_basic_info_list)
    movie_new_db.bulk_execute('INSERT INTO `movie_description`(`internal_id`, `chinese_description`) VALUES (%s,%s)',insert_description_list)
    movie_new_db.bulk_execute('INSERT INTO `movie_other_names`(`movie_name`, `internal_id`) VALUES (%s,%s)',insert_other_movie_titles_list)
    return True

def is_chinese(check_str):
    if '\u4e00' <= check_str <= '\u9fa5':
        return True
    return False
def name_split(ori_name):
    cc = OpenCC('s2tw')
    split_point = False
    for index in range(len(ori_name)-1,0,-1):
        if is_chinese(ori_name[index]) :
            split_point = index
            break
    if split_point:
        chinese_name = cc.convert(ori_name[:split_point+1])
        eng_name = ori_name[split_point+2:]
    else:
        chinese_name = ''
        eng_name = ori_name
    return([chinese_name, eng_name, ori_name])

def insert_actors_to_mysql():
    insert_list = []
    for i in id_data :
        for actor in i['douban_actors_list']:
            actor_name = actor['name']
            insert_list.append(name_split(actor_name))
    if insert_list !=[]:
        movie_new_db.bulk_execute("INSERT ignore INTO `actor_table`( `actor_chinese_name`, `actor_english_name`, `mixed_name`) VALUES (%s, %s, %s)",insert_list)

def insert_directors_to_mysql():
    insert_list = []
    for i in id_data :
        if i['douban_directors_list'] == []:
            director_name = i['backup_director_name']
            try:
                if is_chinese(director_name[0]):
                    insert_list.append([director_name,'',director_name])
                else :
                    insert_list.append(['', director_name, director_name])
            except:
                continue
        for director in i['douban_directors_list']:
            director_name = director['name']
            insert_list.append(name_split(director_name))
    if insert_list !=[]:
        movie_new_db.bulk_execute("INSERT ignore INTO `director_table`(`director_chinese_name`, `director_english_name`, `mixed_name`) VALUES (%s, %s, %s)",insert_list)

    
def insert_movie_feature_relation():
    feature_movie_relation_list= []
    for i in id_data :
        internal_id = i['internal_id']
        for feature in i['category'].split(","):
            if feature not in list(feature_dict.keys()) :
                continue
            feature_id  = feature_dict[feature]
            feature_movie_relation_list.append([feature_id,internal_id])
    movie_new_db.bulk_execute("INSERT INTO `feature_movie_table`(`feature_id`, `internal_id`) VALUES (%s,%s)",feature_movie_relation_list)

def insert_movie_actor_relation():
    actors_list = movie_new_db.fetch_list("SELECT `id`, `mixed_name` FROM `actor_table` ")
    actors_dict ={}
    for i in actors_list :
        actors_dict[i[1]] = i[0]
    actor_movie_relation_list = []
    for i in id_data :
        internal_id = i['internal_id']
        for actor in i['douban_actors_list']:
            actor_id = actors_dict[actor['name']]
            actor_movie_relation_list.append([actor_id,internal_id])
    movie_new_db.bulk_execute("INSERT INTO `actor_movie_relation`(`actor_id`, `internal_id`) VALUES (%s,%s)",actor_movie_relation_list)

def insert_movie_director_relation():
    directors_list = movie_new_db.fetch_list("SELECT `id`, `mixed_name` FROM `director_table` ")
    directors_dict = {}
    for i in directors_list :
        directors_dict[i[1]] = i[0]

    director_movie_relation_list = []
    for i in id_data :
        internal_id = i['internal_id']
        if i['douban_directors_list'] == []:
            try:
                director_id  = directors_dict[i['backup_director_name']]
                director_movie_relation_list.append([director_id,internal_id]) 
            except:
                continue       
        for director in i['douban_directors_list']:
            director_id  = directors_dict[director['name']]
            director_movie_relation_list.append([director_id,internal_id])
    movie_new_db.bulk_execute("INSERT INTO `director_movie_relation`( `director_id`, `internal_id`) VALUES (%s,%s)",director_movie_relation_list)

with DAG('insert_data_into_mysql', default_args=default_args) as dag:

    insert_web_id_relation = PythonOperator(
        task_id = "insert_web_id_relation",
        python_callable = insert_web_id_relation
    )
    insert_movie_basic_info = PythonOperator(
        task_id = "insert_movie_basic_info",
        python_callable = insert_movie_basic_info
    )
    insert_actors_to_mysql = PythonOperator(
        task_id = "insert_actors_to_mysql",
        python_callable = insert_actors_to_mysql
    )
    insert_directors_to_mysql = PythonOperator(
        task_id = "insert_directors_to_mysql",
        python_callable = insert_directors_to_mysql
    )
    insert_movie_feature_relation = PythonOperator(
        task_id = "insert_movie_feature_relation",
        python_callable = insert_movie_feature_relation
    )
    insert_movie_actor_relation = PythonOperator(
        task_id = "insert_movie_actor_relation",
        python_callable = insert_movie_actor_relation
    )
    insert_movie_director_relation = PythonOperator(
        task_id = "insert_movie_director_relation",
        python_callable = insert_movie_director_relation
    )
    check_new_data_insert_status = BranchPythonOperator(
        task_id='check_new_data_insert_status',
        python_callable=check_new_data_insert_status,
    )
    alert_error_insert = PythonOperator(
        task_id = "alert_error_insert",
        python_callable = alert_error_insert
    )
    insert_web_id_relation >> check_new_data_insert_status 
    check_new_data_insert_status >> alert_error_insert
    check_new_data_insert_status >> insert_movie_basic_info >> [insert_actors_to_mysql ,insert_directors_to_mysql]
    insert_movie_basic_info >> insert_movie_feature_relation 
    insert_actors_to_mysql >> insert_movie_actor_relation
    insert_directors_to_mysql >> insert_movie_director_relation
    
