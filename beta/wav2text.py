# ! /usr/bin/env python
# -*- coding:utf-8 -*-

'''
This module will trans Wechat recording file to text via Baidu's API
'''

import base64
import json
import wave
import requests
from pydub import AudioSegment
import pydub


def transcode(file):
    '''File transcode function'''
    rec = AudioSegment.from_mp3(file)
    rec_wav = rec.export(file.replace('mp3', 'wav'), format='wav')
    rec_wav.close()


def get_token():
    '''Get Baidu's api token'''
    _url = 'http://openapi.baidu.com/oauth/2.0/token'
    _params = {'grant_type': 'client_credentials',
               'client_id': 'rqGfWFhPP9s9QQBXllQ7hpVM',  # 改成你自己的
               'client_secret': '88cfa910869ae4c37bb804a0e431cd49'}  # 改成你自己的
    _res = requests.post(_url, _params)
    _data = json.loads(_res.text)
    return _data['access_token']


def wav_to_text(wav_file):
    '''Do recongnize'''
    try:
        wav_file = open(wav_file, 'rb')
    except IOError:
        print('文件错误啊，亲')
        return
    wav_file = wave.open(wav_file)
    n_frames = wav_file.getnframes()
    frame_rate = wav_file.getframerate()
    if n_frames == 1 or frame_rate not in (8000, 16000):
        print('不符合格式')
        return
    audio = wav_file.readframes(n_frames)
    base_data = base64.b64encode(audio).decode('utf-8')
    data = {"format": 'wav',
            "token": get_token(),
            "len": len(audio),
            "rate": frame_rate,
            "speech": base_data,
            "cuid": "B8-AC-6F-2D-7A-94",
            "channel": 1}
    data = json.dumps(data).encode('utf-8')
    res = requests.post('http://vop.baidu.com/server_api',
                        data,
                        {'content-type': 'application/json'})
    res_data = json.loads(res.text)
    print(res_data['result'][0])
    return res_data['result'][0]

if __name__ == '__main__':
    wav_to_text('16k.wav')
