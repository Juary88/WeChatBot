# ! /usr/bin/env python
# -*- coding:utf-8 -*-

import requests

def get_token():
    URL = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
    _header = {'Ocp-Apim-Subscription-Key': 'ee4fc3261b7643dfaff8c04304d9399e'}
    _token = requests.post(url = URL, headers = _header)
    return _token.text

def wav2text():
    url = 'https://speech.platform.bing.com/recognize'
    params = {'Version': '3.0',
              'requestid': 'b2c95ede-97eb-4c88-81e4-80f32d6aee54',
              'appID': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
              'format': 'json',
              'locale': 'zh-CN',
              'device.os': 'Android',
              'scenarios': 'ulm',
              'instanceid':'b2c95ede-97eb-4c88-81e4-80f32d6aee54' }
    d
    recognize = 