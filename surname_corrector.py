#coding:utf-8
'''
Created on 2017-11-21

@author: 刘帅
'''
from pypinyin import pinyin, lazy_pinyin, Style
import re
import itertools
import pickle
import numpy as np
import array


surname_expressions = [
        "口天吴",
        "文刀刘",
        "弓长张",
        "双木林",
        "耳东陈",
        "木子李",
        "立早章",
        "双口吕",
        "三横王",
        "古月胡",
        "木易杨",
        "言午许",
        "美女姜",
        "山高嵩",
        "木公松",
        "水工江",
        "羊女姜",
        "草头黄",
        "双人徐",
        "木土杜",
        "干钩于",
        "子小孙",
        ]

def dict_builder(expressions):
    expressiondict = {}
    
    for expression in expressions:
        multiple_sounds = pinyin(expression, style=Style.FIRST_LETTER, heteronym=False)
        multiple_sounds = list(itertools.chain.from_iterable(multiple_sounds))
        multiple_sounds = "".join(multiple_sounds)
        #print(multiple_sounds)
        #multiple_sounds = itertools.product(multiple_sounds[0], multiple_sounds[1], multiple_sounds[2])
        
        expressiondict[multiple_sounds] = expression[2]
    
    return expressiondict

#namedict = dict_builder(surname_expressions)
#with open('namedict.pickle', 'wb') as handle:
    #pickle.dump(namedict, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
#with open('expressiondict.pickle', 'rb') as handle:
#    expressiondict = pickle.load(handle)
def surname_correct(sentence):
    with open('namedict.pickle', 'rb') as handle:
        expressiondict = pickle.load(handle)
    pysc = sentence[-3:]
    pysc = pinyin(pysc, style=Style.FIRST_LETTER, heteronym=False)
    pysc = list(itertools.chain.from_iterable(pysc))
    pysc = "".join(pysc)
    #print(pysc)
    
    
    final_main_clause = '姓' + expressiondict[pysc]
    return final_main_clause

#expressiondict = dict_builder(surname_expressions)
error_surname_examples = [
        "我姓许，双人需",
        "我姓章，弓长帐"
        ]

for sentence in error_surname_examples:
    corrected_sentence = surname_correct(sentence)
    print('{} now becomes {}'.format(sentence, corrected_sentence))