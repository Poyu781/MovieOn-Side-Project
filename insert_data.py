import dotenv,os,requests
from pymongo import MongoClient
from pprint import pprint
from opencc import OpenCC
from Modules.MySQL_module import SQL

import dotenv

dotenv.load_dotenv()
rds_host = os.getenv("rds_host")
rds_user = os.getenv("rds_user")
rds_password = os.getenv("rds_password")
# local version
client = MongoClient("127.0.0.1:27017",
                     authSource='movie')
cc = OpenCC('s2twp')
db = client['movie']
collection_doubanApi_data = db.douban_raw_json
collection_douban_web_crawl =  db.douban_web_crawl




movie_database = SQL(user=rds_user,password=rds_password,host=rds_host,database="movie")
cursor = collection_douban_web_crawl.find()
# total count  32576
# cursor = collection_doubanApi_data.aggregate([{
#     "$lookup":{
#         "from":"douban_web_crawl",
#         "localField":"id",
#         "foreignField":"Douban_id",
#         "as":"data"
#     }},{"$unwind": "$data"}
#     ])
insert_data_list =[]
# for i in cursor:
#     try:
#         insert_data =[i["Douban_id"], i["IMDb_id"], float(i["avg_rating"]), float(i["ratio_list"][0][:-1]),float(i["ratio_list"][1][:-1]),float(i["ratio_list"][2][:-1]),float(i["ratio_list"][3][:-1]),float(i["ratio_list"][4][:-1]),int(i['rating_amount']),"2021-05-18"]
#         # pprint(insert_data)
#         insert_data_list.append(insert_data)
#     except:
#         continue
# movie_database.bulk_execute("INSERT ignore INTO `Douban_rating`(`Douban_id`, `IMDb_id`, `avg_rating`, `five_star_ratio`, `four_star_ratio`, `three_star_ratio`, `two_star_ratio`, `one_star_ratio`, `total_rating_amount`,`update_date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",insert_data_list)
# cursor1 = collection_doubanApi_data.find()
# for i in cursor1 :
#     try:
#         insert_data = [i["id"],i["title"],i["cover"]]
#         insert_data_list.append(insert_data)
#         # pprint(i)
#     except:
#         continue

# movie_database.bulk_execute("INSERT ignore INTO `Douban_detail`(`Douban_id`,  `movie_title`, `image`) VALUES (%s,%s,%s)",insert_data_list)

result = movie_database.fetch_dict('''SELECT IMDb_rating.rating,Douban_rating.avg_rating, Douban_detail.movie_title,Douban_detail.image    FROM `Douban_rating` left join Douban_detail on Douban_detail.Douban_id = Douban_rating.Douban_idleft join IMDb_rating on Douban_rating.IMDb_id = IMDb_rating.IMDb_id LImit 10''')
pprint(result)


movie_database.fetch_list("select")