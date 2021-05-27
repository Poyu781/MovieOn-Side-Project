from bs4 import BeautifulSoup
from Modules import crawl
import json
from Modules.Mongo_db import movie_mongo_db
import requests
from pprint import pprint
tomato_collection = movie_mongo_db.rottentomato_raw_json

# older fun (new to update)
def rotten_api_fetch(page_num):
    failed_page =[]
    ip_cycle = cycle(ip_list)

    for ip_address in ip_cycle:
        request_url  = f"https://www.rottentomatoes.com/api/private/v2.0/browse?minTomato=10&maxTomato=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page={page_num}"
        proxies = {
            'http': ip_address,
            'https': ip_address,
            }
        headers = {
                'user-agent': ua.random,
                'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
                }  
        req = requests.get(request_url,headers=headers,proxies=proxies)
        print(f"page {page_num} status {req}")
        if req.status_code != 200:
            failed_page.append(page_num)
            print("failed",page_num)
            page_num += 1
            continue

        fetch_json = json.loads(req.text)['results']
        if fetch_json != []:
            collection.insert_many(fetch_json)
            print("success insert")
        else:
            print(fetch_json)
            print("out of list")
            break
        page_num += 1

douban_error_log = open("ErrorLog/tomato_error.json","a")
failed_list =[]
insert_data =[]

def clean_data(fixed_url, search_id,error_file):
    result = crawl.fetch_data(fixed_url, search_id)
    if isinstance(result,dict):
        print(1)
        error_file.write(json.dumps(result) + "\n")
        return "failed"
    try:
        html_text = str(result.find("div",id="mainColumn"))
        if html_text == "None":
            failed_list.append(search_id)
            error_file.write(json.dumps({'id':search_id,"error_msg":"missing content"})+'\n')
            return "failed"
        data = {"id":search_id, "html":html_text}
        insert_data.append(data)
        print("success with ",search_id)
    except Exception as e:
        failed_list.append(search_id)
        error_file.write(json.dumps({'id':search_id,"error_msg":str(e)})+'\n')

crawl.main(clean_data,"https://www.rottentomatoes.com/m/",new_list,douban_error_log)

for i in range(2,5):
    if failed_list != []:
        retry_list = failed_list
        failed_list = []
        douban_error_log.write(f"________failed {i}nd line______\n")
        crawl.main(clean_data,"https://www.rottentomatoes.com/m/",retry_list,douban_error_log)

douban_raw_data  =open("DataSection/tomato_raw_data2.json","a", encoding='utf-8')
douban_raw_data.write(json.dumps(insert_data,ensure_ascii=False))
douban_raw_data.close()
douban_error_log.close()
print("success")


# get the data from file 
def get_data():
    with open("DataSection/tomato_raw_data.json","r") as file:
        # x = file.read()
        # print(x)
        tomato = json.load(file)
    with open("DataSection/tomato_raw_data2.json","r") as file:
        # x = file.read()
        # print(x)
        tomato1 = json.load(file)
    tomato.extend(tomato1)

# get key value from html 
from bs4 import BeautifulSoup
count = 0
tomato_list = []
for i in tomato:
    if i['html'] == 'None' :
        pass
    else :
        html_text = i['html']
        soup = BeautifulSoup(html_text,'html.parser')
        try:
            rotten_id = soup.find("div", id="rating-root").get("data-movie-id")
            title = soup.find("h1", slot="title").text
            director = soup.find(attrs={"data-qa": "movie-info-director"}).text
            tomato_list.append([title,director,rotten_id])
        except:
            print("fa")


# create the title,director dict like {'first love': {'takashi miike': 33098, 'tetsuo shinohara': 16871}}
from collections import defaultdict
check_dict = defaultdict(dict)
for i in movie_director_list:
    title = i[1].lower()
    dire  = i[2].lower()
    check_dict[title][dire] = i[0]

###match data (although work badly)
from pprint import pprint
insert_data = []
# 配對 tomato 跟內部資料
for i in tomato_list :
    match_title_dict = check_dict[i[0].lower()]
    if match_title_dict != {}:
        try :
            if len(match_title_dict)  == 1 :
                internal_id = list(match_title_dict.values())[0]
                insert_data.append([i[2],internal_id])
            else:
                internal_id = match_title_dict[i[1].lower()]
                insert_data.append([i[2],internal_id])
        except Exception as e:
            pprint(match_title_dict)
            pprint(i)
            pprint(e.__class__.__name__)
    else :
        continue


# older version
# faided_id_list = []
# insert_list = []
# error_log = open("error.log","a")
# def crawl_rooten(ip,rotten_id):
#     insert_data = {}
#     try:
#         crawl_url = "https://www.rottentomatoes.com" + rotten_id
#         proxies = {'http': ip, 'https': ip}
#         headers = {'user-agent': ua.random, 'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',}
#         req = requests.get(crawl_url,headers=headers,proxies=proxies) 
#         soup = BeautifulSoup(req.text, 'html.parser')
#         rating_tag = soup.find("score-board")
#         audience_score = rating_tag["audiencescore"]
#         tomatometer_score = rating_tag["tomatometerscore"]
#         tomatometer_review_amount = soup.find("a", slot="critics-count").text
#         audience_review_amount = soup.find("a", slot="audience-count").text
#         print("success "+ rotten_id)
#         insert_data["movie_url"] = rotten_id
#         insert_data["audience_score"] = audience_score
#         insert_data["audience_review_amount"] = audience_review_amount
#         insert_data["tomatometer_score"] = tomatometer_score
#         insert_data["tomatometer_review_amount"] = tomatometer_review_amount
#         insert_list.append(insert_data)
#         # print("----------")
#         # print(crawl_url)
#         # print(audience_score,audience_review_amount)
#         # print(tomatometer_score,tomatometer_review_amount)
#         # print("----------")
#     except Exception as e:
#         print("failed"+crawl_url)
#         faided_id_list.append(rotten_id)
#         if e.__class__.__name__ != "TypeError":
#             error_log.write(str(e)+"\n")
#             error_log.write(crawl_url)


# def thread_crawler(fun,ip_list,id_list):
    # threads =[]
    # start_time = time.time()
    # # r = 0
    # for ip,json in zip(ip_list,id_list):
    #     threads.append(threading.Thread(target = fun, args = (ip,json["url"])))
    #     time.sleep(0.5)
    #     threads[-1].start()
    #     # r += 1
    #     # if r == 200 :
    #     #     break
    # # r = 0
    # for i in range(343):
    #     # print(threads[i])
    #     threads[i].join()
    #     # r += 1
    #     # if r == 200 :
    #     #     break
    # print(time.time() - start_time)