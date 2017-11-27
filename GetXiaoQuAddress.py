#coding:utf-8
'''
Created on 2017-11-27

@author: 刘帅
'''
# #coding:utf-8

import requests
import json

def GetAddress(keywords,city):
#url = "http://restapi.amap.com/v3/place/text?key=f1296fe56c973f62be07915f935178b2&keywords=京东花园&types=小区&city=泰州&children=&offset=&page=&extensions=all"
    payload = {'keywords': keywords, 'key': 'f1296fe56c973f62be07915f935178b2','city':city,'types':'小区'}
    r = requests.get("http://restapi.amap.com/v3/place/text", params=payload)
    parsed_j = json.loads(r.text)
    if(len(parsed_j['pois']) > 0):
        print(parsed_j['pois'][0]['name']) #返回匹配最高的小区名字
        print(parsed_j['pois'][0]['address'])#返回具体地址
        print(parsed_j['pois'][0]['pname'])#返回省份
        print(parsed_j['pois'][0]['adname'])#返回区
        
GetAddress("京东花园","泰州")
