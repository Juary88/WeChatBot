#coding:utf-8
'''
Created on 2017-11-21

@author: 刘帅
'''
from jpype import * 
import re
startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.3.4.jar;D:\hanlp", "-Xms1g", "-Xmx1g") # 启动JVM，Linux需替换分号;为冒号:
def findAddress(string):
    ad = ''
    ad2 = ''
    ad3 = ''
    HanLP = JClass('com.hankcs.hanlp.HanLP')
    #sentence = "江苏省泰州市海淀区，然后是新泰路街道，然后是锦东花苑7小区然后8栋401你好"
    list = HanLP.newSegment().enablePlaceRecognize(True).seg(string);
    pattern = re.compile(r'[0-9_-_零_一_二_三_四_五_六_七_八_九_十]*小区')
    pattern2 = re.compile(r'[0-9_-_零_一_二_三_四_五_六_七_八_九_十]*(栋|单元|号楼|号铺|座|室|号|楼|#|门面|店面)')
    #pattern3 = re.compile(r'[0-9_-_零_一_二_三_四_五_六_七_八_九_十]{2,4}')
    p = re.compile(r'[0-9_-_零_一_二_三_四_五_六_七_八_九_十]{2,4}')
    #print p.findall('one1two2three3four4')
    match = pattern.search(string)
    if match:
        ad = match.group()
    match2 = pattern2.search(string)
    if match2:
        ad2 = match2.group()
    match3 = p.findall(string)
    #print(match3)
    if match3:
        ad3 = match3[-1]
    add = []
    for name in list:
        #print(str(name.nature))
        if str(name.nature) == 'ns' or name.word == '市' or name.word == '区':
            #print(name.word)
            add.append(str(name.word).replace("\ns",""))
    print("".join(add) + ad + ad2 + ad3)
    address = "".join(add) + ad + ad2 + ad3
    return address
#findAddress("江苏省泰州市海淀区，然后是新泰路街道，然后是锦东花苑7小区然后儿二单元401-3333你好")
