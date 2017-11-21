#
'''
Created on 2017-11-17

@author: 刘帅
'''
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = 'test_python'
API_KEY = '***********'
SECRET_KEY = '**********'

def textToMp3(text):
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    # 读取文件
    result  = aipSpeech.synthesis(text, 'zh', 1, {
        'vol': 5,
    })
    voice = 'auido.mp3'
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(voice, 'wb') as f:
            f.write(result)
    return voice
