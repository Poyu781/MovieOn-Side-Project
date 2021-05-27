import dotenv,os,requests
from pymongo import MongoClient
import requests,json
from fake_useragent import UserAgent
from itertools import cycle
from Modules.crawl import ip_list
from Modules.Mongo_db import movie_mongo_db


collection_api = movie_mongo_db.douban_raw_json_2021

ua = UserAgent(verify_ssl=False)
def douban_api_fetch(start_year,end_year,start_num):
    ip_cycle = cycle(ip_list)
    failed_num_list = []
    for ip_address in ip_cycle:
        request_url  = f"https://movie.douban.com/j/new_search_subjects?sort=U&range=2,10&tags=%E7%94%B5%E5%BD%B1&start={start_num}&year_range={start_year},{end_year}"
        proxies = {
            'http': ip_address,
            'https': ip_address,
            }
        headers = {
                'user-agent': ua.random,
                'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
                }  
        req = requests.get(request_url,headers=headers,proxies=proxies)
        print(f"page {start_num} status {req}")
        try:
            fetch_json = json.loads(req.text)['data']
            # print(fetch_json)
            if fetch_json != []:
                collection_api.insert_many(fetch_json)
                print("success insert")
            else:
                print(fetch_json)
                print("out of list")
                break
        except:
            failed_num_list.append(start_num)
            print("failure with" ,start_num)
        start_num += 20


douban_api_fetch(2021,2021,0)