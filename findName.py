#coding:utf-8
'''
Created on 2017-11-22

@author: 刘帅
'''

from jpype import *
startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.3.4.jar;D:\hanlp", "-Xms1g", "-Xmx1g") # 启动JVM，Linux需替换分号;为冒号:
def extract_name(string):

    name = ""
    
    HanLP = JClass('com.hankcs.hanlp.HanLP')
    
    list = HanLP.newSegment().enablePlaceRecognize(True).seg(string);
    print(list)
    for name in list:
    #print(str(name.nature))
        if str(name.nature) == 'nr' or str(name.nature) == 'nx':
            #print(name.word)
            name = str(name.word).replace("\ns","")
            
            return name

extract_name("我姓林")   

