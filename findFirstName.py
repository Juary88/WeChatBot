#coding:utf-8
'''
Created on 2017-11-23

@author: 刘帅
'''
import re
def extract_firstName(string):
    pattern = re.compile(r'[(姓)(叫我)(叫)(称呼我)(称呼)].{2}')
    match = pattern.search(string)
    if match:
        #print(match.group()[1:])
        return(match.group()[2:])
    return None