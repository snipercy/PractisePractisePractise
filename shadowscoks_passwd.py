# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import socket
import requests
import json
import re


socket.setdefaulttimeout(10)

request_params = {'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
                  }

# 发送链接请求
def do_request(url):
    while True:
        try:
            r = requests.get(url, request_params)
            if r.status_code != 200:
                print ("Http request error: " + str(r.status_code) + " ---- " + url)
                return ""
            return r.content
        except Exception:
            continue

# 写入指定文件
def output_to_file(file, info):
    for item in info:
        file.write(item.encode('utf-8').replace('\n', '').replace('\r', '').replace(' ', '') + ", ")
    file.write('\n')

def ss(url):
    ret = do_request(url)
    ret_info = []

    soup = BeautifulSoup(ret,'lxml')
    free = soup.find(name='section',id='free')
    h4 = free.find_all(name='h4',limit=4)
    for cur in h4 :
        cur.text.encode('utf-8')
        cur_text = cur.text.split(":")[1].encode('utf-8')
        # for debug
        # print cur_text
        ret_info.append(cur_text) # [name, port , passwd, encrypt]

    return ret_info[2]

def set_passwd(url,ss_conf):
    passwd = ss(url)
    data = open(ss_conf)
    print(data)
    r = json.load(data)
    print r
    r["name"]["subname"] = "subtest"
    print "after", r

    return passwd


if __name__ == '__main__':
    url = 'http://www.ishadowsocks.net'
    ss_conf = 'json.json'
    print(set_passwd(url,ss_conf))

