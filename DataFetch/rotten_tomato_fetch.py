import dotenv,os,requests
from pymongo import MongoClient
import requests,json
from fake_useragent import UserAgent
from itertools import cycle
import threading,time
import requests,json
from fake_useragent import UserAgent
from itertools import cycle
from bs4 import BeautifulSoup
ip_list = ['http://tihyjcyk-dest:sr9mbjac4xab@45.146.180.69:9139', 'http://tihyjcyk-dest:sr9mbjac4xab@45.128.247.174:7675', 'http://tihyjcyk-dest:sr9mbjac4xab@45.94.47.121:8165', 'http://tihyjcyk-dest:sr9mbjac4xab@85.209.130.100:7641', 'http://tihyjcyk-dest:sr9mbjac4xab@45.137.43.47:7601', 'http://tihyjcyk-dest:sr9mbjac4xab@45.142.28.114:8125', 'http://tihyjcyk-dest:sr9mbjac4xab@45.137.84.15:7065', 'http://tihyjcyk-dest:sr9mbjac4xab@91.246.193.60:6317', 'http://tihyjcyk-dest:sr9mbjac4xab@45.154.56.114:7132', 'http://tihyjcyk-dest:sr9mbjac4xab@91.246.194.18:6531', 'http://tihyjcyk-dest:sr9mbjac4xab@193.23.253.69:7641', 'http://tihyjcyk-dest:sr9mbjac4xab@193.27.10.145:6230', 'http://tihyjcyk-dest:sr9mbjac4xab@5.154.253.30:8288', 'http://tihyjcyk-dest:sr9mbjac4xab@185.95.157.83:6104', 'http://tihyjcyk-dest:sr9mbjac4xab@45.128.245.61:9072', 'http://tihyjcyk-dest:sr9mbjac4xab@193.5.251.127:7634', 'http://tihyjcyk-dest:sr9mbjac4xab@45.154.58.50:7563', 'http://tihyjcyk-dest:sr9mbjac4xab@109.207.130.19:8026', 'http://tihyjcyk-dest:sr9mbjac4xab@45.9.122.183:8264', 'http://tihyjcyk-dest:sr9mbjac4xab@2.56.101.189:8721', 'http://tihyjcyk-dest:sr9mbjac4xab@185.245.27.157:6930', 'http://tihyjcyk-dest:sr9mbjac4xab@5.157.130.247:8251', 'http://tihyjcyk-dest:sr9mbjac4xab@185.245.27.137:6910', 'http://tihyjcyk-dest:sr9mbjac4xab@37.35.40.139:8229', 'http://tihyjcyk-dest:sr9mbjac4xab@176.116.231.146:7488', 'http://tihyjcyk-dest:sr9mbjac4xab@91.246.192.118:6119', 'http://tihyjcyk-dest:sr9mbjac4xab@193.27.23.101:9189', 'http://tihyjcyk-dest:sr9mbjac4xab@176.116.230.111:7197', 'http://tihyjcyk-dest:sr9mbjac4xab@185.245.26.2:6519', 'http://tihyjcyk-dest:sr9mbjac4xab@200.0.61.74:6149', 'http://tihyjcyk-dest:sr9mbjac4xab@37.35.41.124:8470', 'http://tihyjcyk-dest:sr9mbjac4xab@185.205.194.228:7748', 'http://tihyjcyk-dest:sr9mbjac4xab@193.8.231.198:9204', 'http://tihyjcyk-dest:sr9mbjac4xab@45.154.244.47:8085', 'http://tihyjcyk-dest:sr9mbjac4xab@84.21.188.31:8565', 'http://tihyjcyk-dest:sr9mbjac4xab@64.43.91.183:6954', 'http://tihyjcyk-dest:sr9mbjac4xab@64.43.90.82:6597', 'http://tihyjcyk-dest:sr9mbjac4xab@185.95.157.166:6187', 'http://tihyjcyk-dest:sr9mbjac4xab@45.137.43.35:7589', 'http://tihyjcyk-dest:sr9mbjac4xab@185.205.194.175:7695', 'http://tihyjcyk-dest:sr9mbjac4xab@45.154.84.72:8123', 'http://tihyjcyk-dest:sr9mbjac4xab@85.209.129.127:8667', 'http://tihyjcyk-dest:sr9mbjac4xab@200.0.61.213:6288', 'http://tihyjcyk-dest:sr9mbjac4xab@45.137.40.176:8729', 'http://tihyjcyk-dest:sr9mbjac4xab@37.35.40.188:8278', 'http://tihyjcyk-dest:sr9mbjac4xab@176.116.230.61:7147', 'http://tihyjcyk-dest:sr9mbjac4xab@45.87.249.192:7770', 'http://tihyjcyk-dest:sr9mbjac4xab@37.35.40.185:8275', 'http://tihyjcyk-dest:sr9mbjac4xab@5.154.253.219:8477', 'http://tihyjcyk-dest:sr9mbjac4xab@5.157.130.77:8081', 'http://tihyjcyk-dest:sr9mbjac4xab@45.131.212.146:6195', 'http://tihyjcyk-dest:sr9mbjac4xab@5.154.253.155:8413', 'http://tihyjcyk-dest:sr9mbjac4xab@176.116.231.110:7452', 'http://tihyjcyk-dest:sr9mbjac4xab@193.23.253.82:7654', 'http://tihyjcyk-dest:sr9mbjac4xab@45.92.247.84:6592', 'http://tihyjcyk-dest:sr9mbjac4xab@45.130.60.81:9608', 'http://tihyjcyk-dest:sr9mbjac4xab@85.209.129.114:8654', 'http://tihyjcyk-dest:sr9mbjac4xab@45.131.212.68:6117', 'http://tihyjcyk-dest:sr9mbjac4xab@2.56.101.175:8707', 'http://tihyjcyk-dest:sr9mbjac4xab@85.209.130.145:7686', 'http://tihyjcyk-dest:sr9mbjac4xab@45.86.15.18:8565', 'http://tihyjcyk-dest:sr9mbjac4xab@5.154.253.114:8372', 'http://tihyjcyk-dest:sr9mbjac4xab@193.23.253.88:7660', 'http://tihyjcyk-dest:sr9mbjac4xab@193.23.253.115:7687', 'http://tihyjcyk-dest:sr9mbjac4xab@45.72.55.201:7238', 'http://tihyjcyk-dest:sr9mbjac4xab@45.72.55.127:7164', 'http://tihyjcyk-dest:sr9mbjac4xab@45.72.55.200:7237', 'http://tihyjcyk-dest:sr9mbjac4xab@45.72.55.174:7211', 'http://tihyjcyk-dest:sr9mbjac4xab@45.130.60.129:9656', 'http://tihyjcyk-dest:sr9mbjac4xab@45.130.60.228:9755', 'http://tihyjcyk-dest:sr9mbjac4xab@45.130.60.123:9650', 'http://tihyjcyk-dest:sr9mbjac4xab@2.56.101.136:8668', 'http://tihyjcyk-dest:sr9mbjac4xab@45.92.247.166:6674', 'http://tihyjcyk-dest:sr9mbjac4xab@45.131.212.244:6293', 'http://tihyjcyk-dest:sr9mbjac4xab@185.95.157.190:6211', 'http://tihyjcyk-dest:sr9mbjac4xab@45.87.249.197:7775', 'http://tihyjcyk-dest:sr9mbjac4xab@185.95.157.131:6152', 'http://tihyjcyk-dest:sr9mbjac4xab@45.131.212.246:6295', 'http://tihyjcyk-dest:sr9mbjac4xab@45.87.249.15:7593', 'http://tihyjcyk-dest:sr9mbjac4xab@45.92.247.197:6705', 'http://tihyjcyk-dest:sr9mbjac4xab@2.56.101.219:8751', 'http://tihyjcyk-dest:sr9mbjac4xab@45.130.60.107:9634', 'http://tihyjcyk-dest:sr9mbjac4xab@185.95.157.117:6138', 'http://tihyjcyk-dest:sr9mbjac4xab@45.131.212.138:6187', 'http://tihyjcyk-dest:sr9mbjac4xab@45.92.247.141:6649', 'http://tihyjcyk-dest:sr9mbjac4xab@45.92.247.241:6749', 'http://tihyjcyk-dest:sr9mbjac4xab@45.87.249.249:7827', 'http://tihyjcyk-dest:sr9mbjac4xab@193.151.160.57:8144', 'http://tihyjcyk-dest:sr9mbjac4xab@193.151.160.143:8230', 'http://tihyjcyk-dest:sr9mbjac4xab@193.151.161.119:8462', 'http://tihyjcyk-dest:sr9mbjac4xab@193.151.161.60:8403']
dotenv.load_dotenv()
mongo_server = os.getenv("mongo_server")
mongo_user = os.getenv("mongo_user")
mongo_password = os.getenv("mongo_password")

client = MongoClient(mongo_server,
                     username=mongo_user,
                     password=mongo_password,
                     authSource='movie',
                     authMechanism='SCRAM-SHA-1')

db = client['movie']
collection = db.rottentomato_raw_json
page_num =0
ua = UserAgent(verify_ssl=False)
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

faided_id_list = []
insert_list = []
error_log = open("error.log","a")
def crawl_rooten(ip,rotten_id):
    insert_data = {}
    try:
        crawl_url = "https://www.rottentomatoes.com" + rotten_id
        proxies = {'http': ip, 'https': ip}
        headers = {'user-agent': ua.random, 'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',}
        req = requests.get(crawl_url,headers=headers,proxies=proxies) 
        soup = BeautifulSoup(req.text, 'html.parser')
        rating_tag = soup.find("score-board")
        audience_score = rating_tag["audiencescore"]
        tomatometer_score = rating_tag["tomatometerscore"]
        tomatometer_review_amount = soup.find("a", slot="critics-count").text
        audience_review_amount = soup.find("a", slot="audience-count").text
        print("success "+ rotten_id)
        insert_data["movie_url"] = rotten_id
        insert_data["audience_score"] = audience_score
        insert_data["audience_review_amount"] = audience_review_amount
        insert_data["tomatometer_score"] = tomatometer_score
        insert_data["tomatometer_review_amount"] = tomatometer_review_amount
        insert_list.append(insert_data)
        # print("----------")
        # print(crawl_url)
        # print(audience_score,audience_review_amount)
        # print(tomatometer_score,tomatometer_review_amount)
        # print("----------")
    except Exception as e:
        print("failed"+crawl_url)
        faided_id_list.append(rotten_id)
        if e.__class__.__name__ != "TypeError":
            error_log.write(str(e)+"\n")
            error_log.write(crawl_url)


def thread_crawler(fun,ip_list,id_list):
    threads =[]
    start_time = time.time()
    # r = 0
    for ip,json in zip(ip_list,id_list):
        threads.append(threading.Thread(target = fun, args = (ip,json["url"])))
        time.sleep(0.5)
        threads[-1].start()
        # r += 1
        # if r == 200 :
        #     break
    # r = 0
    for i in range(343):
        # print(threads[i])
        threads[i].join()
        # r += 1
        # if r == 200 :
        #     break
    print(time.time() - start_time)