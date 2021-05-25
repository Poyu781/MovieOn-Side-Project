import json
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup
import threading,time
import requests
import tenacity
from config import ip_list
ua = UserAgent(verify_ssl=False)

def error_handle(fun):
    def wrapper(*args):
        try :
            return fun(*args)
            # insert_data.append(soup.find("strong",property="v:average").text)
        except Exception as e:
            return {"id":args[-1],"msg":str(e)}
    return wrapper


@error_handle
@tenacity.retry(reraise=True,stop=tenacity.stop_after_attempt(5))
def fetch_data(fixed_url, search_id):
    ip = random.choice(ip_list)
    crawl_url = fixed_url + search_id
    print(crawl_url)
    proxies = {'http': ip, 'https': ip}
    headers = {'user-agent': ua.random, 'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',}
    req = requests.get(crawl_url,headers=headers,proxies=proxies)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup



def start_thread(threads,fun,*args):
    threads.append(threading.Thread(target = fun, args = (args)))
    time.sleep(0.01)
    threads[-1].start()

# def clean_data(fixed_url, search_id,error_file):
#     result = fetch_data(fixed_url, search_id)
#     if isinstance(result,dict):
#         error_file.write(json.dumps(result) + "\n")
#         return "failed"
#     print(result.find("strong",property="v:average").text)
# douban_error_log = open("douban_error.json","a")
# id_list = ['25728006',"34973399"]
def main(fun, fixed_url, id_list, error_log):
    threads =[]
    for id in id_list:
        start_thread(threads,fun,fixed_url, id, error_log)
    for i in threads:
        i.join()
# main(clean_data,"https://movie.douban.com/subject/",id_list,douban_error_log)

