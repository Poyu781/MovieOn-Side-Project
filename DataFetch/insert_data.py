import dotenv,os,requests
from pymongo import MongoClient
from pprint import pprint
# from opencc import OpenCC
from Modules.MySQL_module import SQL

import dotenv

dotenv.load_dotenv()
rds_host = os.getenv("rds_host")
rds_user = os.getenv("rds_user")
rds_password = os.getenv("rds_password")
# local version

movie_database = SQL(user=rds_user,password=rds_password,host=rds_host,database="movie")


if __name__ == "__main__":
    client = MongoClient("127.0.0.1:27017",
                     authSource='movie')
    cc = OpenCC('s2twp')
    db = client['movie']
    collection_doubanApi_data = db.douban_raw_json
    collection_douban_web_crawl =  db.douban_web_crawl
    
    cursor = collection_douban_web_crawl.find()
# total count  32576
    def dunban_fetch():
        cursor = collection_doubanApi_data.aggregate([{
            "$lookup":{
                "from":"douban_web_crawl",
                "localField":"id",
                "foreignField":"Douban_id",
                "as":"data"
            }},{"$unwind": "$data"}
            ])
        insert_data_list =[]
        for i in cursor:
            try:
                insert_data =[i["Douban_id"], i["IMDb_id"], float(i["avg_rating"]), float(i["ratio_list"][0][:-1]),float(i["ratio_list"][1][:-1]),float(i["ratio_list"][2][:-1]),float(i["ratio_list"][3][:-1]),float(i["ratio_list"][4][:-1]),int(i['rating_amount']),"2021-05-18"]
                # pprint(insert_data)
                insert_data_list.append(insert_data)
            except:
                continue
        movie_database.bulk_execute("INSERT ignore INTO `Douban_rating`(`Douban_id`, `IMDb_id`, `avg_rating`, `five_star_ratio`, `four_star_ratio`, `three_star_ratio`, `two_star_ratio`, `one_star_ratio`, `total_rating_amount`,`update_date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",insert_data_list)
        cursor1 = collection_doubanApi_data.find()
        for i in cursor1 :
            try:
                insert_data = [i["id"],i["title"],i["cover"]]
                insert_data_list.append(insert_data)
                # pprint(i)
            except:
                continue

# movie_database.bulk_execute("INSERT ignore INTO `Douban_detail`(`Douban_id`,  `movie_title`, `image`) VALUES (%s,%s,%s)",insert_data_list)

# result = movie_database.fetch_dict('''SELECT IMDb_rating.rating,Douban_rating.avg_rating, Douban_detail.movie_title,Douban_detail.image    FROM `Douban_rating` left join Douban_detail on Douban_detail.Douban_id = Douban_rating.Douban_idleft join IMDb_rating on Douban_rating.IMDb_id = IMDb_rating.IMDb_id LImit 10''')
# pprint(result)

    def put_rotten_rating():
        r = db.rotten_tomato_rating.aggregate([{
            "$lookup":{
                "from":"rottentomato_raw_json",
                "localField":"movie_url",
                "foreignField":"url",
                "as":"data"
            }},{"$unwind": "$data"}
            ])
        insert_list = []
        count = 0
        for i in r :
            title = i['data']['title'].lower() 
            if title in movie_list :
                id = str(i['data']['id'])
                imdb_id = movie_dict[title]
                audience_score = i['audience_score']
                audience_amount = i['audience_review_amount']
                tomator_amount = i['tomatometer_review_amount']
                tomator_score = i['tomatometer_score']
                # if "," in audience_amount :
                #     audience_amount = int(audience_amount.replace(",", ""))
                # else:
                #     audience_amount = int(audience_amount)
                # tomator_amount = i['tomatometer_review_amount'].split(" ")[0]
                # if "," in tomator_amount :
                #     tomator_amount = int(tomator_amount.replace(",", ""))
                # else:
                #     tomator_amount = int(tomator_amount)
                insert_data = [id,imdb_id,audience_score, audience_amount,tomator_score,tomator_amount ]
                insert_list.append(insert_data)
            #     count += 1
            # if count >10 :
            #     break
        print("start insrt")


    def put_douban_detail():
        mongo_data = db.douban_web_crawl.find()
        insert_list = []
        for i in mongo_data:
            try :
                insert_data = [i['IMDb_id'], i["other_names"], i["description"],i["Douban_id"]]
                insert_list.append(insert_data)
            except:
                continue

        print(len(insert_list))

    # insert 
    movie_database.bulk_execute("UPDATE `douban_detail` SET`imdb_id`=%s,`other_names`=%s,`movie_description`=%s WHERE douban_id = %s",insert_list[10000:])

    def fetch_newest_data():
        result = movie_database.fetch_list("SELECT rotten_tomato_rating.imdb_id ,rotten_tomato_rating.audience_rating,rotten_tomato_rating.tomator_rating,imdb_rating.rating,douban_rating.avg_rating FROM `rotten_tomato_rating` left join imdb_rating on imdb_rating.imdb_id = rotten_tomato_rating.imdb_id left join douban_rating on douban_rating.imdb_id = rotten_tomato_rating.imdb_id limit 1")

    movie_database.bulk_execute("INSERT INTO `movie_latest_rating` ( `imdb_id`, `tomato_audience_rating`, `tomator_rating`,`imdb_rating`,`douban_rating`, `ptt_rating`, `update_time`) VALUES ( %s,%s,%s,%s,%s,'null', '2021-05-17')",(result[0]))