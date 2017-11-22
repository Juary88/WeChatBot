# coding: utf-8


import itchat
from itchat.content import TEXT
from itchat.content import RECORDING
import requests
import threading
from findAddressName import findAddress
import requests
import json
name = ''
phone_number = ''
address=''

def extract_entities(query_str):
    # sample input: "天津市和平区西康路37号赛顿中心。"
    # its output： ['天津市', '和平区', '西康路', '37号', '赛顿中心']
    response = requests.post("http://192.168.2.171:5002/parse", '{{"q":"{0}", "project": "default", "model": "model_20171121-135555"}}'.format(query_str).encode('utf-8'))
    parsed_j = json.loads(response.text)
    print(parsed_j)
    intent = parsed_j["intent"]['name']
    print(intent)
    if intent == "phone_number":
        
        #print(intent)
        values = [e["value"] for e in parsed_j["entities"]]
        return intent,values[0]
         #print(intent)
    
    if(intent == "greet"):
            
            #values = [e["value"] for e in parsed_j["entities"]]
        return intent,intent
    if(parsed_j['intent']['name']=="address"):
        values = [e["value"] for e in parsed_j["entities"]]
        #print("".join(values))
        return parsed_j['intent']['name'],"".join(values)
    return "null","null"
# todo 用另一个进程把服务起来
bot_api="http://127.0.0.1:8000/get_response"

# 带对象参数注册，对应消息对象将调用该方法
@itchat.msg_register(TEXT, isFriendChat=True )
def text_reply(msg):
    user_input = msg['Text']
    #print(user_input)
    user_input = user_input.replace(",","")
    print(user_input)
    payload={"user_input":user_input}
    intent,entity= extract_entities(user_input)
    if(intent == "phone_number"):
        phone_number =  entity
    #print(phone_number)
        itchat.send("好的，您的电话是" + str(phone_number), msg['FromUserName'])
    if(intent == "greet"):
        itchat.send("您好，感谢您访问夏普公司，很高兴为您服务。", msg['FromUserName'])
    if(intent == "address"):
        address = findAddress(user_input)
        itchat.send("您的地址是" + str(address), msg['FromUserName'])
    if(intent == "null"):#处理地址intent识别错误就用hanlp
        address = findAddress(user_input)
        itchat.send("您的地址是" + str(address), msg['FromUserName'])
    #response = requests.get(bot_api,params=payload).json()["response"]
    #itchat.send(response, msg['FromUserName'])

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
            response = "好的，您的电话是" + str(phone_number)
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
            address = findAddress(text)
            response = "您的地址是" + str(address)
            filename2 = textToMp3.textToMp3(response)
        
            reply = itchat.send_file('D:/tomcat/wechat_bot-master/auido.mp3', msg['FromUserName'])
            print(reply['BaseResponse']['ErrMsg'])
        #response = requests.get(bot_api,params=payload).json()["response"]
        #filename2 = textToMp3.textToMp3(response)
        
        #reply = itchat.send_file('D:/tomcat/wechat_bot-master/auido.mp3', msg['FromUserName']) 
        #print(reply['BaseResponse']['ErrMsg'])
    
# 把服务跑起来 bottlell
def bot_server():
    from bottle import Bottle,run
    from bottle import response,request
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from json import dumps

    deepThought = ChatBot("deepThought",read="only")
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


