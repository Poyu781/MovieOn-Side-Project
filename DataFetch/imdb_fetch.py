import requests
import urllib.request
import ssl
import gzip
from Modules.MySQL_module import SQL


# from Modules.MySQL_module import SQL
class IMDb_fetch():
    ssl._create_default_https_context = ssl._create_unverified_context
    INSTALL_PATH = "DataSection/"
    def __init__(self,file_url,file_name):
        self.file_url = file_url
        self.file_name = file_name
    
    def install_data(self):
        print('Beginning file download with urllib2...')
        urllib.request.urlretrieve(self.file_url, self.INSTALL_PATH + self.file_name)
    
    def decompress_file(self):
        file_path = self.INSTALL_PATH + self.file_name
        out_list = []
        with gzip.open(file_path) as f:
            file_content = f.read().decode("utf-8")
            data = file_content.split("\n")
            for line in data[0:20] :
                out_list.append(line.split('\t'))
            f.close()
        return out_list

movie_rate = IMDb_fetch("https://datasets.imdbws.com/title.ratings.tsv.gz","movie_rate.tsv.gz")
movie_rate.install_data()
x = movie_rate.decompress_file()
print(x[:12])

# movie_detail = IMDb_fetch("https://datasets.imdbws.com/title.basics.tsv.gz","movie_detail.tsv.gz")
# movie_detail.install_data()
# x = movie_detail.decompress_file()
# print(x[:12])



# url = "https://datasets.imdbws.com/title.ratings.tsv.gz"



# urllib.request.urlretrieve(url, '/Users/poyuchiu/Desktop/MovieOn/DataSection/rate.tsv.gz')
# with gzip.open('/Users/poyuchiu/Desktop/MovieOn/DataSection/rate.tsv.gz') as f:
#     file_content = f.read().decode("utf-8")
#     data = file_content.split("\n")
#     print(data[0:15])
#     f.close()
    # print(len(f))
    # f[-1] = f[-1] +'\n'
    # r = 0
    # for i in f:
    #     split_data = i.split("\t")
    #     try:
    #         if split_data[1] == "movie" and  split_data[5] != '\\N' and int(split_data[5]) == 2021:
    #             split_data[-1] = split_data[-1][:-2]
    #             r += 1
    #             print(split_data)
    #     except:
    #         print(split_data)
    # print(r)

# with open("/Users/poyuchiu/Desktop/MovieOn/DataSection/rate.tsv","w") as file:
#     file.write(file_content)
#     file.close()

# with open("/Users/poyuchiu/Desktop/MovieOn/DataSection/rate.tsv","r") as file:
#     print(file.readlines()[3:15])
#     file.close()

