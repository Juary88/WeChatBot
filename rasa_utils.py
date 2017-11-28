# -*- coding: utf-8 -*-

import requests
import json

def extract_entities(query_str):
    # sample input: "天津市和平区西康路37号赛顿中心。"
    # its output： ['天津市', '和平区', '西康路', '37号', '赛顿中心']
    response = requests.post("http://192.168.2.171:5002/parse", '{{"q":"{0}", "project": "default", "model": "model_20171126-064026"}}'.format(query_str).encode('utf-8'))
    parsed_j = json.loads(response.text)
    values = [e["value"] for e in parsed_j["entities"]]
    return values
