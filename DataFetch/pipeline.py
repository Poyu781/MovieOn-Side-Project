from imdb_fetch import IMDb_fetch, insert_movie_rating_to_mysql, insert_movie_detail_to_mongo
import datetime
import os

today_date = datetime.datetime.today().date()
movie_detail_file_exist_boolean = os.path.isfile(
    f'./DataSection/movie_detail{today_date}.tsv.gz')

imdb_movie_datail_data = IMDb_fetch(
    "https://datasets.imdbws.com/title.basics.tsv.gz", "movie_detail")

if not movie_detail_file_exist_boolean:
    imdb_movie_datail_data.install_data()
    data = imdb_movie_datail_data.decompress_file()
else:
    data = imdb_movie_datail_data.decompress_file()

imdb_list = insert_movie_detail_to_mongo(data[:100], 1900, 2021, "movie")
print(imdb_list)


from collections import defaultdict
from bs4 import BeautifulSoup
def get_data_from_douban_html(douban_data):
    for i in douban_data:
        try:
            insert_data = defaultdict(list)
            douban_id = i['id']
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