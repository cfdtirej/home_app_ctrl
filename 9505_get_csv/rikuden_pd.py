import csv
import requests
from datetime import datetime

url = 'http://www.rikuden.co.jp/nw/denki-yoho/csv/juyo_05_20201226.csv'
res = requests.get(url)
res.encoding = res.apparent_encoding
data = [[t for t in txt.split(',')] for txt in res.text.splitlines()]
print(data)
# data = [i for i in res.text.splitlines()]
# print(data)
# print(res.text.rs.splitlines())
# data_list = [string for string in res.text.splitlines()]
# print(data_list)
# for i in
# for data
# with open('./data.csv', 'w') as f:
#     writer = csv.writer(f)
