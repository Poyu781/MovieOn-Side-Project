import sys
import os,json
import time
import re
import urllib
from pprint import pprint
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import defaultdict
from difflib import SequenceMatcher

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from modules import crawl
from modules import mail_notification
from modules.imdb_fetch import IMDb_fetch,BASE_DIR,movie_mongo_db
default_args = {
    'owner': 'Poyu',
    'start_date': datetime(2021, 6, 26, 0, 0),
    'schedule_interval': '@daily',
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

def match_douban_id(fixed_url, search_id,error_file):
    result = crawl.fetch_data(fixed_url, search_id,"json")
    # print(result)
    # pprint(result)
    try:
        for i in result['items']:
            link = i['link']
            try:
                douban_id = re.search(r'subject/[0-9].*?/', link)[0][8:-1]
            except:
                continue
            if search_id in i['snippet'] : 
                collection.update( { "imdb_id" : search_id },{ "$set" : { 'douban_id' :douban_id} } , upsert=True)
                print("success",search_id,"__",douban_id)
                douban_id_list.append(douban_id)
                break
    except Exception as e:
        print(e)
        collection.update( { "imdb_id" : search_id },{ "$set" : { 'douban_id' : None} } , upsert=True)
        print("error",search_id)
today_date = datetime.today().date()
collection = movie_mongo_db["data_"+str(today_date)]
def download_imdb_movie_detail():
    
    file_path = os.path.join(BASE_DIR, 'data/download_data/')
    movie_detail_file_exist_boolean = os.path.isfile(f'{file_path}/movie_detail{today_date}.tsv.gz')
    try :
        imdb_movie_datail_data = IMDb_fetch("https://datasets.imdbws.com/title.basics.tsv.gz","movie_detail",today_date)
        imdb_movie_datail_data.install_data()
        return True
    except:
        return False
    

def insert_movie_detail_to_mongo(start_year, end_year, feature_type, **context):

    download_data_boolean = context['task_instance'].xcom_pull(task_ids='download_imdb_movie_detail')
    if not download_data_boolean :
        print("didn't have file to insert")
        return False
    
    imdb_movie_datail_data = IMDb_fetch("https://datasets.imdbws.com/title.basics.tsv.gz","movie_detail",today_date)
    data = imdb_movie_datail_data.decompress_file()


    file_path = os.path.join(BASE_DIR, 'data/exist_movie_id.json')
    with open(file_path,"r") as file :
        existed_movie_list = json.load(file)
    
    movie_detail_list = []
    imdb_id_list = []
    for i in data:
        insert_dict = {}
        movie_detail_info = i.split("\t")
        try:
            if  movie_detail_info[1] == feature_type and movie_detail_info[0] not in existed_movie_list and movie_detail_info[5] != '\\N' and movie_detail_info[7] != '\\N' and int(movie_detail_info[5]) >= start_year and int(movie_detail_info[5]) <= end_year:
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
    print(len(movie_detail_list))
    if movie_detail_list != []:
        collection.insert_many(movie_detail_list)
        print("success insert into mongodb")
        print(len(imdb_id_list))
        existed_movie_list.extend(imdb_id_list)
        with open(file_path,"w") as file :
            file.write(json.dumps(existed_movie_list,ensure_ascii=False))
    return imdb_id_list



def check_new_data_exist(**context):
    anything_new = context['task_instance'].xcom_pull(task_ids='insert_movie_detail_to_mongo')

    print("Does new films update？")
    if anything_new  == []:
        return 'send_email_when_imdb_does_not_have_new_data_to_update'
    else:
        return 'multiple_thread_match_douban_id'

douban_id_list = []

def send_email_when_imdb_does_not_have_new_data_to_update():
    text = f'''
    Today Airflow Fetch Success !

    It seem today didn't have data need to update ,please check !
    '''
    mail_notification.send_email(f"Notification! Daily Airflow Report - {today_date}",text)

def multiple_thread_match_douban_id (**context):
    imdb_id_list = context['task_instance'].xcom_pull(task_ids='insert_movie_detail_to_mongo')
    if imdb_id_list :
        crawl.main(match_douban_id,"https://www.googleapis.com/customsearch/v1/siterestrict?cx=493c9af9b59e1e9c8&key=AIzaSyC2pJ7kme6oCPsxe-ZAyOsCsxdKPgK7r1g&q=",imdb_id_list,"r.log")
        print("suc")
        return douban_id_list
    else :
        print("didn't get imdb_id_list")
        return False


def check_douban_match(**context):
    douban_match_result = context['task_instance'].xcom_pull(task_ids='multiple_thread_match_douban_id')

    print("Does new films update？")
    if douban_match_result != [] :
        return 'multiple_thread_store_douban_web_data'
    else:
        return 'send_email_when_movie_does_not_match_douban'

def send_email_when_movie_does_not_match_douban(**context):
    imdb_id_list = context['task_instance'].xcom_pull(task_ids='insert_movie_detail_to_mongo')
    text = f'''
    Today Airflow Fetch Success !
    However, these imdb_id didn't match any douban id ,
    please check {imdb_id_list}
    '''
    mail_notification.send_email(f"Notification! Daily Airflow Report - {today_date}",text)





def multiple_thread_store_douban_web_data(**context):
    douban_id_list = context['task_instance'].xcom_pull(task_ids='multiple_thread_match_douban_id')
    if douban_id_list == [] :
        print("doesn't have douban_id")
        return False
    error_file_path = os.path.join(BASE_DIR, 'data/error_json/douban_error.json')
    douban_error_log = open(error_file_path,"a")
    failed_list =[]
    insert_data =[]
    def store_douban_web_data(fixed_url, search_id,error_file):
        result = crawl.fetch_data(fixed_url, search_id)
        if isinstance(result,dict):
            print(1)
            error_file.write(json.dumps(result) + "\n")
            return "failed"
        try:
            data = {"douban_id":search_id, "html":str(result.find("div",class_="article")),"json" : result.find('script', type='application/ld+json').string }
            insert_data.append(data)
            print("success with ",search_id)
        except Exception as e:
            failed_list.append(search_id)
            error_file.write(json.dumps({'douban_id':search_id,"error_msg":str(e)})+'\n')
    crawl.main(store_douban_web_data,"https://movie.douban.com/subject/",douban_id_list,douban_error_log)

    for i in range(2,5):
        if failed_list != []:
            retry_list = failed_list
            failed_list = []
            douban_error_log.write(f"________failed {i}nd line______\n")
            crawl.main(store_douban_web_data,"https://movie.douban.com/subject/",retry_list,douban_error_log)

    download_douban_file_path = os.path.join(BASE_DIR, f'data/download_data/douban_web_data_{today_date}.json')
    douban_raw_data = open(download_douban_file_path,"a", encoding='utf-8')
    douban_raw_data.write(json.dumps(insert_data,ensure_ascii=False))
    douban_raw_data.close()
    douban_error_log.close()
    print("success")
    return True




def get_data_from_douban_json(douban_data):
    for i in douban_data:
        actors_list = []
        directors_list = []
        authors_list = []
        try :
            douban_movie_data = i['json']
            douban_json_data = json.loads(douban_movie_data,strict=False)

            douban_id = douban_json_data['url'].split('/')[2]
            movie_title = douban_json_data['name']
            img = douban_json_data['image']
            feature_list = douban_json_data['genre']
            published_date  = douban_json_data["datePublished"]
            for actor in douban_json_data['actor'][:5]:
                actors_list.append(actor)
            for director in douban_json_data['director']:
                directors_list.append(director)
            for author in douban_json_data['author']:
                authors_list.append(author)
            collection.update( 
                { "douban_id" : douban_id },
                { "$set" : 
                    { 
                    'douban_image' :img,
                    'douban_movie_title':movie_title,
                    'douban_published_date':published_date,
                    'douban_feature_list':feature_list,
                    'douban_actors_list':actors_list,
                    'douban_directors_list':directors_list,
                    'douban_authors_list':authors_list,
                    } 
                } , upsert=True)
            print("success insert json with " + douban_id)
        except Exception as e:
            print(e.__class__.__name__,e,f"failed with {douban_id}")
def get_data_from_douban_html(douban_data):
    for i in douban_data:
        try:
            insert_data = defaultdict(list)
            douban_id = i['douban_id']
            soup = BeautifulSoup(i['html'], 'html.parser')
            info = soup.find("div",id="info").text
            split_info = info.split("\n")[1:-1]
            for i in split_info :
                if i[:2] == "导演" :
                    insert_data["dirctor"] = i[4:]  
                elif i[:2] == "制片" :
                    insert_data["country"] = i[9:]
                if i[:2] == "又名":
                    insert_data["other_names"] = i[4:]
            try:
                insert_data['desc'] = soup.find("span",property="v:summary").text
            except:
                insert_data['desc'] = None
            collection.update( 
            { "douban_id" : douban_id },
            { "$set" : 
                { 
                'backup_director_name' :insert_data['dirctor'],
                'douban_movie_country':insert_data["country"],
                'douban_movie_other_names':insert_data["other_names"],
                'douban_description':insert_data['desc']
                } 
            } , upsert=True)
            print("success",douban_id)
        except Exception as e:
            print(douban_id)
            print(e.__class__.__name__,e)
def get_data_from_douban():
    douban_data_file_path = os.path.join(BASE_DIR, f'data/download_data/douban_web_data_{today_date}.json')
    with open(douban_data_file_path,"r") as file:
        douban_data = json.load(file)
    get_data_from_douban_json(douban_data)
    get_data_from_douban_html(douban_data)
    return True



def match_actor_name(douban_actor_list,tomato_actor_list,pass_threshold):
    count = 0
    tomato_len = len(tomato_actor_list)
    for douban_name in douban_actor_list:
        for tomato_name in tomato_actor_list:
            
            sim_ratio = SequenceMatcher(None, douban_name, tomato_name).ratio()
            # print(douban_name,tomato_name,sim_ratio)
            # print(douban_name,tomato_name,sim_ratio)
            if sim_ratio >= 0.9 :
                count += 1
                # print(douban_name,"__",tomato_name)
    # print(count)
    if count >= pass_threshold :
        # print(count)
        return True
def match_title(douban_title,tomato_title):
    sim_ratio = SequenceMatcher(None, douban_title.lower(), tomato_title.lower()).ratio()
    return sim_ratio
def str_has_chinese(check_str):
    for i in check_str: 
        if '\u4e00' <= i <= '\u9fa5':
            return False
    return True

def get_match_data():
    mongo_data = collection.find({ "douban_id": { "$ne": None } } )
    tomato_search_dict = {}
    for i in mongo_data :
        douban_info_dict = defaultdict(list)
        for actor_dict in i['douban_actors_list']:
            douban_info_dict['actors_split_list'].extend(actor_dict['name'].split(" "))
        if i['douban_directors_list'] == []:
            douban_info_dict['directors_split_list'].append(i['backup_director_name'])
        else:
            for director_dict in i['douban_directors_list']:
                douban_info_dict['directors_split_list'].extend(director_dict['name'].split(" "))
        for author_dict in i['douban_authors_list']:
            douban_info_dict['authors_split_list'].extend(author_dict['name'].split(" "))

        
        movie_names_list = []
        movie_names_list.extend(i['douban_movie_title'].split(" ", 1))
        if i['douban_movie_other_names'] != [] :
            movie_names_list.extend(i['douban_movie_other_names'].split(" / "))
        if  i['original_title'] not in movie_names_list:
            movie_names_list.append(i['original_title'])
        if i['primary_title'] not in movie_names_list:
            movie_names_list.append(i['primary_title'])
        for title in movie_names_list :
            if str_has_chinese(title) :
                douban_info_dict['movie_names_list'].append(title)

        douban_info_dict['published_country'] = i['douban_movie_country']
        tomato_search_dict[i['douban_id']] = douban_info_dict
    return tomato_search_dict
    print("suc")

def get_douban_tomato_relateion(url,douban_id,error_file):
    actors_name_list = tomato_search_dict[douban_id]['actors_split_list']
    # print(name_list)
    movie_title = tomato_search_dict[douban_id]['movie_names_list'][0]
    lenght_of_title = len(movie_title)
    fetch_json = crawl.fetch_data(url,urllib.parse.quote(movie_title),"json")
    result = fetch_json['movies']['items']
    count = fetch_json['movies']['count']
    if count  == 0:
        print("doesn't have any matches !")
        return False
    for data in result :
        tomato_actor_list = " ".join(data['cast']).split(" ")
        # print(tomato_actor_list)
        if match_title(movie_title,data['name']) == 1:
            if match_actor_name(actors_name_list,tomato_actor_list,3):
    
                print("success !",douban_id)
                collection.update( { "douban_id" : douban_id },{ "$set" : { 'rotten_tomato_url' :data['url']} } , upsert=True)
                return True
    match = False
    for data in result :
        tomato_actor_list = " ".join(data['cast']).split(" ")
        len_of_title = min(lenght_of_title,len(data['name']))
        # print(movie_title[:len_of_title],'\n',data['name'][:len_of_title],'\n',movie_title[-len_of_title:],'\n',data['name'][-len_of_title:],'\n')
        if match_title(movie_title[:len_of_title], data['name'][:len_of_title]) >= 0.7 or match_title(movie_title[-len_of_title:], data['name'][-len_of_title:]) >= 0.7:
            match = True
            cast_match_result = match_actor_name(actors_name_list,tomato_actor_list,2)
            # print(cast_match_result)
            if cast_match_result :

                rotten_already_exist = collection.find({"$and":[{"douban_id":douban_id},{"rotten_tomato_url": {'$exists': True}}]}).count()
                if rotten_already_exist < 1:
                    print("success !",douban_id)
                # print("success !"
                    collection.update( { "douban_id" : douban_id },{ "$set" : { 'rotten_tomato_url' :data['url']} } , upsert=True)
                    return True       
    if match:
        for data in result :
            if match_title(movie_title,data['name']) > 0.95 and count <=2  :
                rotten_already_exist = collection.find({"$and":[{"douban_id":douban_id},{"rotten_tomato_url": {'$exists': True}}]}).count()
                if rotten_already_exist < 1:
                    print("success !",douban_id)
                    collection.update( { "douban_id" : douban_id },{ "$set" : { 'rotten_tomato_url' :data['url']} } , upsert=True)
                    return True   
        collection.update( { "douban_id" : douban_id },{ "$set" : { 'rotten_tomato_url' :None} } , upsert=True)
        print("title match but cast didn't match well,please check[",movie_title,douban_id)
        return False
    else:
        collection.update( { "douban_id" : douban_id },{ "$set" : { 'rotten_tomato_url' :None} } , upsert=True)
        print("doesn't match",movie_title,douban_id)#

tomato_search_dict = {}
def multiple_thread_match_douban_tomato_id(**context):
    global tomato_search_dict 
    tomato_search_dict = get_match_data()

    crawl.main(get_douban_tomato_relateion,"https://www.rottentomatoes.com/napi/search/all?type=movie&searchQuery=",list(tomato_search_dict.keys()),"r.log")



douban_tomato_relation_dict = {}
def get_douban_tomato_relation_dict():
    data = collection.find({"$and":[{"douban_id":{'$exists': True}},{"rotten_tomato_url": {'$ne': None}}]})
    douban_tomato_relation_dict = {}
    for i in data:
        douban_tomato_relation_dict[i['douban_id']] = i['rotten_tomato_url'].split("/")[-1]

    return douban_tomato_relation_dict

def multiple_thread_download_tomato_web_data():
    global douban_tomato_relation_dict 
    douban_tomato_relation_dict = get_douban_tomato_relation_dict()
    if douban_tomato_relation_dict == {}:
        print("doesn't have data")
        return False
    error_file_path = os.path.join(BASE_DIR, 'data/error_json/tomato_error.json')
    tomato_error_log = open(error_file_path,"a")
    failed_list =[]
    insert_data =[]
    def download_tomato_web_data(fixed_url, search_id,error_file):

        search_name = douban_tomato_relation_dict[search_id]
        result = crawl.fetch_data(fixed_url, search_name)
        if isinstance(result,dict):
            error_file.write(json.dumps(result) + "\n")
            return "failed"
        try:
            html_text = str(result.find("div",id="mainColumn"))
            if html_text == "None":
                failed_list.append(search_id)
                error_file.write(json.dumps({'douban_id':search_id,"title":search_name,"error_msg":"missing content"})+'\n')
                return "failed"
            data = {"douban_id":search_id, "title":search_name,"html":html_text}
            insert_data.append(data)
            print("success with ",search_id)
        except Exception as e:
            failed_list.append(search_id)
            error_file.write(json.dumps({'douban_id':search_id,"title":search_name,"error_msg":str(e)})+'\n')
    crawl.main(download_tomato_web_data,"https://www.rottentomatoes.com/m/",list(douban_tomato_relation_dict.keys()),tomato_error_log)#['2131664'],douban_error_log)
    print(len(insert_data))
    for i in range(2,5):
        
        if failed_list != []:
            print("b",failed_list)
            retry_list = failed_list
            failed_list = []
            tomato_error_log.write(f"________failed {i}nd line______\n")
            crawl.main(download_tomato_web_data,"https://www.rottentomatoes.com/m/",retry_list,tomato_error_log)
    print(len(insert_data))        
    download_tomato_file_path = os.path.join(BASE_DIR, f'data/download_data/tomato_web_data_{today_date}.json')
    douban_raw_data  = open(download_tomato_file_path,"a", encoding='utf-8')
    douban_raw_data.write(json.dumps(insert_data,ensure_ascii=False))
    douban_raw_data.close()
    tomato_error_log.close()
    if len(insert_data) >= 1:
        return True


def get_data_from_tomato_html(**context):
    tomato_id_list = []
    check_json_data_exist = context['task_instance'].xcom_pull(task_ids='multiple_thread_download_tomato_web_data')
    if not check_json_data_exist :
        return False
    tomato_data_file_path = os.path.join(BASE_DIR, f'data/download_data/tomato_web_data_{today_date}.json')
    with open(tomato_data_file_path,"r") as file:
        tomato_data = json.load(file)
    for i in tomato_data:
        if i['html'] == 'None' :
            continue
        else :
            try:
                html_text = i['html']
                soup = BeautifulSoup(html_text,'html.parser')
                # rotten_id = soup.find("div", id="rating-root").get("data-movie-id")
                douban_id = i['douban_id']
                try :
                    director = soup.find(attrs={"data-qa": "movie-info-director"}).text
                except:
                    director = None
                collection.update( { "douban_id" : douban_id },{ "$set" : { 'rotten_director_name' :director,'rotten_tomato_id': i['title']} } , upsert=True)
                tomato_id_list.append(i['title'])
                print(douban_id,rotten_id,director)
            except Exception as e:
                print(e)
                print(i['title'])
                    # print(soup.find("h1", class_="scoreboard__title"))
                print(douban_id)
                print("fail")
                continue
    return True,tomato_id_list

def send_email_to_check_result():
    today_total_new_data = collection.find().count()
    douban_found_data = collection.find({"douban_id":{'$ne': None}}).count()
    tomato_found_data = collection.find({"rotten_tomato_id":{'$exists': True}}).count()
    text = f'''
    Today Airflow Fetch Success ! Data Already store in MongoDB
    New data from IMDb : {today_total_new_data}
    New data from Douban : {douban_found_data}
    New data from RottenTomato : {tomato_found_data}
    '''
    mail_notification.send_email(f"Daily Airflow Report - {today_date}",text)


with DAG('fetch_movie_data', default_args=default_args) as dag:

    download_imdb_movie_detail = PythonOperator(
        task_id = "download_imdb_movie_detail",
        python_callable = download_imdb_movie_detail
    )
    
    insert_movie_detail_to_mongo = PythonOperator(
        task_id = "insert_movie_detail_to_mongo",
        python_callable = insert_movie_detail_to_mongo,
        op_args=[2021,2021,"movie"]
    )
    multiple_thread_match_douban_id = PythonOperator(
        task_id = "multiple_thread_match_douban_id",
        python_callable = multiple_thread_match_douban_id,
    )

    check_douban_match = BranchPythonOperator(
        task_id='check_douban_match',
        python_callable=check_douban_match,
    )
    send_email_when_movie_does_not_match_douban = PythonOperator(
        task_id = "send_email_when_movie_does_not_match_douban",
        python_callable = send_email_when_movie_does_not_match_douban
    )


    multiple_thread_store_douban_web_data = PythonOperator(
        task_id = "multiple_thread_store_douban_web_data",
        python_callable = multiple_thread_store_douban_web_data,

    )
    check_new_data_exist = BranchPythonOperator(
        task_id='new_movie_available',
        python_callable=check_new_data_exist,
    )
    send_email_when_imdb_does_not_have_new_data_to_update = PythonOperator(
        task_id = "send_email_when_imdb_does_not_have_new_data_to_update",
        python_callable = send_email_when_imdb_does_not_have_new_data_to_update
    )
    # trigger_clean_douban_dag = TriggerDagRunOperator(
    #     task_id="trigger_clean_douban_dag",
    #     trigger_dag_id="clean_douban_tomato_data", 
    # )
    
    get_data_from_douban = PythonOperator(
        task_id = "get_data_from_douban",
        python_callable = get_data_from_douban
    )

    multiple_thread_match_douban_tomato_id = PythonOperator(
        task_id = "multiple_thread_match_douban_tomato_id",
        python_callable = multiple_thread_match_douban_tomato_id
    )
    multiple_thread_download_tomato_web_data = PythonOperator(
        task_id = "multiple_thread_download_tomato_web_data",
        python_callable = multiple_thread_download_tomato_web_data
    )
    get_data_from_tomato_html = PythonOperator(
        task_id = "get_data_from_tomato_html",
        python_callable = get_data_from_tomato_html
    )

    send_email_to_check_result = PythonOperator(
        task_id = "send_email_to_check_result",
        python_callable = send_email_to_check_result
    )

    download_imdb_movie_detail >> insert_movie_detail_to_mongo  >> check_new_data_exist
    check_new_data_exist >> multiple_thread_match_douban_id >> check_douban_match
    check_new_data_exist >> send_email_when_imdb_does_not_have_new_data_to_update  
    check_douban_match >> multiple_thread_store_douban_web_data >> get_data_from_douban
    check_douban_match >> send_email_when_movie_does_not_match_douban
    get_data_from_douban >> multiple_thread_match_douban_tomato_id >> multiple_thread_download_tomato_web_data >> get_data_from_tomato_html >> send_email_to_check_result