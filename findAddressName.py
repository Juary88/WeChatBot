#coding:utf-8
'''
Created on 2017-11-21

@author: 刘帅
'''
from jpype import * 
import re
startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.3.4.jar;D:\hanlp", "-Xms1g", "-Xmx1g") # 启动JVM，Linux需替换分号;为冒号:
HanLP = JClass('com.hankcs.hanlp.HanLP')
sentence = "江苏省泰州市海淀区，然后是新泰路街道，然后是锦东花苑7小区然后8栋二单元401你好"
list = HanLP.newSegment().enablePlaceRecognize(True).seg(sentence);
pattern = re.compile(r'[0-9_-_零_一_二_三_四_五_六_七_八_九_十]*小区.*[栋|号楼|座|号院]')
match = pattern.search(sentence)
if match:
    print(match.group())
add = []
for name in list:
    #print(str(name.nature))
    if str(name.nature) == 'ns' or name.word == '市' or name.word == '区':
        #print(name.word)
        add.append(str(name.word).replace("\ns",""))
print("".join(add))

