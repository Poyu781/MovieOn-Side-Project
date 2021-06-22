from pprint import pprint
from random import randrange
from Modules import crawl
import json
from Modules.Mongo_db import movie_mongo_db



douban_collection = movie_mongo_db.douban_raw_json_2021
id_list = []
for i in douban_collection.find({},{"id":1}):
    id_list.append(i['id'])

print("ok")
print(len(id_list))


douban_error_log = open("ErrorLog/douban_error.json","a")
douban_raw_data  =open("DataSection/douban_web_data4.json","a", encoding='utf-8')
failed_list =[]
insert_data =[]
index = 0
def clean_data(fixed_url, search_id,error_file):
    result = crawl.fetch_data(fixed_url, search_id)
    if isinstance(result,dict):
        print(1)
        error_file.write(json.dumps(result) + "\n")
        return "failed"
    try:
        data = {"id":search_id, "html":str(result.find("div",class_="article")),"json" : result.find('script', type='application/ld+json').string }
        insert_data.append(data)
        print("success with ",search_id)
    except Exception as e:
        failed_list.append(search_id)
        error_file.write(json.dumps({'id':search_id,"error_msg":str(e)})+'\n')

crawl.main(clean_data,"https://movie.douban.com/subject/",id_list,douban_error_log)


for i in range(2,5):
    if failed_list != []:
        retry_list = failed_list
        failed_list = []
        douban_error_log.write(f"________failed {i}nd line______\n")
        crawl.main(clean_data,"https://movie.douban.com/subject/",retry_list,douban_error_log)


douban_raw_data.write(json.dumps(insert_data,ensure_ascii=False))
douban_raw_data.close()
douban_error_log.close()
print("success")


















# v1 code
# ip_cycle = cycle(ip_list)
# ua = UserAgent(verify_ssl=False)
# faided_id_list =[]
# attribute_error_list = []
# insert_list = []
# successed_id_list = []
# error_log = open("error.log","a")


# def crawl_douban(ip,Douban_id):
#     crawl_url = "https://movie.douban.com/subject/" + Douban_id
#     proxies = {'http': ip, 'https': ip}
#     headers = {'user-agent': ua.random, 'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',}  
#     try :
#         req = requests.get(crawl_url,headers=headers,proxies=proxies)
#         if req.status_code == 200:
#             insert_data = {}
#             insert_data["Douban_id"] = Douban_id
#             soup = BeautifulSoup(req.text, 'html.parser')
#             rating_ratio_list =soup.find("div",class_="ratings-on-weight").find_all("span",class_= "rating_per")
#             insert_data["ratio_list"] = []
#             for ratio in rating_ratio_list :
#                 insert_data["ratio_list"].append(ratio.text)
            
#             insert_data["description"] = soup.find("span",property="v:summary").text.replace("\n","").replace("\u3000\u3000","")
            
#             avg_rating = soup.find("strong",property="v:average").text
#             rating_amount = soup.find("span",property="v:votes").text

#             insert_data["avg_rating"] = avg_rating
#             insert_data["rating_amount"] = rating_amount
#             # print(info)

#             info = soup.find("div",id="info").text
#             split_info = info.split("\n")[1:-1]

#             for i in split_info :
#                 if i[:2] == "编剧" :
#                     insert_data["writers"] = i[4:]  
#                 elif i[:2] == "类型":
#                     insert_data["category"] = i[4:]
#                 elif i[:2] == "制片" :
#                     insert_data["country"] = i[9:]
#                 elif i[:2] == "又名":
#                     insert_data["other_names"] = i[4:]
#                 elif i[:6] == "IMDb链接" :
#                     insert_data["IMDb_id"] = i[8:]
#                 elif i[:4] == "IMDb":
#                     insert_data["IMDb_id"] = i[6:]
#             insert_list.append(insert_data)

            
#             successed_id_list.append(Douban_id)
#             print("Success",Douban_id)
#         else:
#             error_log.write(f"failed with {Douban_id}\n")
#             faided_id_list.append(Douban_id)
#             print(Douban_id,"failed !")
#     except Exception as e:
#         if e.__class__.__name__ == "AttributeError":
#             attribute_error_list.append(Douban_id)
#             print("not text error ",Douban_id)
#         else:
#             faided_id_list.append(Douban_id)
#             error_log.write(str(e)+"\n")
#             error_log.write(f"error with {Douban_id}\n")
#             print("error with ",Douban_id)


# def thread_crawler(fun,ip_list,id_list):
#     threads =[]
#     start_time = time.time()
#     r = 0
#     for ip,json in zip(ip_list,id_list):
#         threads.append(threading.Thread(target = crawl_douban, args = (ip,json["id"])))
#         time.sleep(0.2)
#         threads[-1].start()
#         # r += 1
#         # if r == 200 :
#         #     break
#     r = 0
#     for i in range(len(id_list)):
#         # print(threads[i])
#         threads[i].join()
#         # r += 1
#         # if r == 200 :
#         #     break
#     print(time.time() - start_time)

# db.douban_web_crawl.insert_many(insert_list)