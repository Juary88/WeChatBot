# coding: utf-8

#from wxbot import WXBot
import itchat
from itchat.content import TEXT
from itchat.content import RECORDING
import requests
import threading
from findAddressName import findAddress
from findFirstName import extract_firstName
import requests
import json
import findFirstName
import re
from GetXiaoQuAddress import GetAddress
from surname_corrector import surname_correct
name = ''
phone_number = ''
address=''
address_detail = ''
type = ''
install_place = ''
date = ''
xiaoqu = ''
province = ''
dis_qu = ''
confidence = 0
price = 0

tmp = ''
import re
def getAllNumber(query_str):
    return "".join(re.findall(r"\d+\.?\d*",query_str))
    
def extract_entities(query_str):
    # sample input: "天津市和平区西康路37号赛顿中心。"
    # its output： ['天津市', '和平区', '西康路', '37号', '赛顿中心']  
    response = requests.post("http://192.168.2.171:5002/parse", '{{"q":"{0}", "project": "default", "model": "model_20171207-164652"}}'.format(query_str).encode('utf-8'))
    parsed_j = json.loads(response.text)
    print(parsed_j)
    intent = parsed_j["intent"]['name']
    entity_dict = {e["entity"]: e["value"] for e in parsed_j["entities"]}
    values = [e["value"] for e in parsed_j["entities"]]
    global confidence#全局变量
    
    confidence = parsed_j["intent"]['confidence']
    print(intent)
    print(confidence)
    if intent=="install":
        return "install","install"
    if intent == "inform" and "install_place" in entity_dict:
        return intent,entity_dict["install_place"]
    if intent == "signal" and confidence > 0.31:
        return intent,intent
    if intent == "inform" and "date" in entity_dict:
       return intent,entity_dict["date"]
    if ('LCD' in tmp and '看看' not in query_str) or intent=="finding":
       if len(getAllNumber(query_str)) == 0:
          return "getsize","getsize"
    if '到家了吗' in tmp:
       if '没' in query_str or '快' in query_str or intent=="nottohome":
          return "notArrive","notArrive"
    if '电视信号' in tmp:
       if '没' in query_str or intent=="nosignal":
          return "notSignal","notSignal"
    if intent == "inform" \
        and ("size" in entity_dict \
        or "phone" in entity_dict \
        or "install_wall_type" in entity_dict):
        number = getAllNumber(query_str)
        if len(number) >= 10:
           intent = "phone_number"
           return intent,number
        else:
            print(tmp + "666")
            if('两种收费' in tmp):
               intent = "price"
               return intent,number
            elif(len(number) == 3):#直接就说数字的，无法理解是哪个意思
               intent = "unknown"
               return intent,intent
            elif(len(number) == 2):
               intent = "size"
               return intent,number
            elif(len(number) > 0):
               intent = "install_type"
               return intent,query_str
         #print(intent)
    if intent == "inform" and "name" in entity_dict:
        return intent,intent 
    if intent == "greet":
            
            #values = [e["value"] for e in parsed_j["entities"]]
        return intent,intent
    if intent == "inform" and "address" in entity_dict:
        #print("".join(values))
        return "address","".join(values)
    return "null","null"
# todo 用另一个进程把服务起来
bot_api="http://127.0.0.1:8000/get_response"

# 带对象参数注册，对应消息对象将调用该方法
@itchat.msg_register(TEXT, isFriendChat=True )
def text_reply(msg):
    global tmp
    user_input = msg['Text']
    #print(user_input)
    user_input = user_input.replace(",","")
    print(user_input)
    payload={"user_input":user_input}
    intent,entity= extract_entities(user_input)
    if(intent == "phone_number"):
        phone_number =  entity
    #print(phone_number)
        itchat.send("好的，您的电话是" + str(phone_number)+"," +"那您的安装地址哪里呢?", msg['FromUserName'])
    elif(intent == "greet"):
        itchat.send("您好，感谢您访问夏普公司，很高兴为您服务。", msg['FromUserName'])
    elif(intent == "address"):
        address,xiaoqu,city,dis_qu2,dong = findAddress(user_input)
        address = entity
        xiaoqu,address_detail,province,dis_qu= GetAddress(xiaoqu,city)
        if(len(dis_qu) > 0):
          address = province + city + dis_qu2 + xiaoqu + address_detail + dong
          itchat.send("您的地址是" + str(address), msg['FromUserName'])
        else:
          itchat.send("您的地址是" + str(address), msg['FromUserName'])
    elif(intent == "name"):
        name = surname_correct(user_input)
        if name == "":
           name = extract_firstName(user_input)
        tmp = "请问您的电视机到家了吗?"
        itchat.send("好的，" + str(name) + "先生，请问您的电视机到家了吗？", msg['FromUserName'])
    elif(intent == "install_type"):
        type = entity
        tmp = "好的，您的电视型号是" + str(type) + "那请问您的电视是要放在柜子上还是挂在墙上呢？"
        itchat.send(tmp, msg['FromUserName'])
    elif(intent == "install_place"):
        install_place = entity
        tmp = "挂在墙上是有两种收费的，一种是简单固定型的是210元，另外一种是裝壁伸缩型可以微调的是550元，那您要选择哪一种呢"
        print(tmp)
        itchat.send(tmp, msg['FromUserName'])
    elif(intent == "signal"):
        print(confidence)
        tmp = "好的，您的信号已经开通了，请问您的电视机型号可以提供一下吗？是以LCD-开头的"
        itchat.send(tmp, msg['FromUserName'])
    elif(intent == "date"):
        date = entity
        itchat.send("好的，那到时候师傅上门是联系您本人吗？", msg['FromUserName'])
    elif(intent == "install"):
        itchat.send("好的，请问您贵姓呢怎么称呼您呢", msg['FromUserName'])
    elif(intent == "hanger"):
        tmp = "好的，您的信号已经开通了，请问您的电视机型号可以提供一下吗？是以LCD-开头的"
        itchat.send(tmp, msg['FromUserName'])
    elif(intent == "price"):
        price = entity
        itchat.send("好的，您选取的安装方式费用为" + str(price) + "那现在为您预约，从明天开始，哪天方便哪" , msg['FromUserName'])
    elif(intent == "getsize"):
        tmp = "请问您的电视机尺寸是多少呢？"
        itchat.send(tmp,msg['FromUserName'])
    elif(intent == "size"):
        size = entity
        itchat.send("您的电视机尺寸是" + str(size) + "请问您的电视是要放在柜子上还是挂在墙上呢？" , msg['FromUserName'])
    elif(intent == "notArrive"):
        tmp = ""
        itchat.send("为了避免师傅上门时电视还没有送到家无法安装，建议您等电视送到家后再来电报装。" , msg['FromUserName'])
    elif(intent == "notSignal"):
        tmp = ""
        itchat.send("师傅上门安装后还会为您调试，如果信号没有开通就无法进行调试，后续调试的话可能会产生费用，所以建议您等信号开通后再来电报装。" , msg['FromUserName'])
    elif(confidence < 0.31):
        response = requests.get(bot_api,params=payload).json()["response"]
        tmp = response
        itchat.send(response, msg['FromUserName'])

@itchat.msg_register(RECORDING)
def rec_reply(msg):
    # 是否开启语音识别，需要安装ffmpeg和pydub
        msg['Text']('./records/' + msg['FileName'])
        
        from beta import wav2text,textToMp3
        wav2text.transcode('./records/' + msg['FileName'])
        filename = msg['FileName'].replace('mp3','wav')
        text = wav2text.wav_to_text('./records/' + filename)
        text = text.replace(",","")
        print(text)
        payload={"user_input":text}
        intent,entity= extract_entities(text)
        if(intent == "phone_number"):
            phone_number =  entity
            response = "好的，您的电话是" + str(phone_number) + "," +"那您的安装地址哪里呢?"
            filename2 = textToMp3.textToMp3(response)
        
            reply = itchat.send_file('D:/tomcat/wechat_bot-master/auido.mp3', msg['FromUserName']) 
        #print(phone_number)
            #itchat.send("好的，您的电话是" + str(phone_number), msg['FromUserName'])
        if(intent == "greet"):
            response = "您好，感谢您访问夏普公司，很高兴为您服务。"
            filename2 = textToMp3.textToMp3(response)
        
            reply = itchat.send_file('D:/tomcat/wechat_bot-master/auido.mp3', msg['FromUserName'])
            print(reply['BaseResponse']['ErrMsg'])
            #itchat.send("您好，感谢您访问夏普公司，很高兴为您服务。", msg['FromUserName'])
        if(intent == "address"):
            address = findAddress(text)
            response = "您的地址是" + str(address)
            filename2 = textToMp3.textToMp3(response)
            print(reply['BaseResponse']['ErrMsg'])
            reply = itchat.send_file('D:/tomcat/wechat_bot-master/auido.mp3', msg['FromUserName']) 
        if(intent == "null"):#处理地址intent识别错误就用hanlp
            #address = findAddress(text)
            #response = "您的地址是" + str(address)
            #filename2 = textToMp3.textToMp3(response)
        
            #reply = itchat.send_file('D:/tomcat/wechat_bot-master/auido.mp3', msg['FromUserName'])
            #print(reply['BaseResponse']['ErrMsg'])
            response = requests.get(bot_api,params=payload).json()["response"]
            filename2 = textToMp3.textToMp3(response)
            print(response)
            reply = itchat.send_file('D:/tomcat/wechat_bot-master/auido.mp3', msg['FromUserName']) 
            print(reply['BaseResponse']['ErrMsg'])
    
# 把服务跑起来 bottlell
def bot_server():
    from bottle import Bottle,run
    from bottle import response,request
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from json import dumps

    deepThought = ChatBot("deepThought",read_only=True)
    deepThought.set_trainer(ChatterBotCorpusTrainer)
    # 使用中文语料库训练它
    # 只需要训练一次，不需要每次启动进程都训练，训练结果默认存到本地`./database.db`,之后启动进程会使用这个数据库
    #deepThought.train("chatterbot.corpus.custom")  # 语料库

    app = Bottle()
    @app.route('/get_response')
    def get_response():
        user_input = request.query.user_input or ""
        d_response = deepThought.get_response(user_input).text
        response.content_type = 'application/json'
        res = {"response":d_response}
        return dumps(res)

    run(app, host='localhost', port=8000)



botThread = threading.Thread(target=bot_server)
botThread.setDaemon(True)
botThread.start()

itchat.auto_login(hotReload=True)
itchat.run()

