# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 13:45:45 2017

@author: user
"""

from pypinyin import pinyin, lazy_pinyin, Style
import re
import itertools
import pickle

def extend_one_sound(sound):
    extended_sound = [sound]
            
    #extend consonants
    # for example, see 'z', 'zh' as the same sound
    consonants = ['ㄓ', 'ㄔ', 'ㄕ', 'ㄗ', 'ㄘ', 'ㄙ']
    if sound[0] in consonants:
        new_consonant = consonants[(consonants.index(sound[0])+3)%len(consonants)]
        extended_sound.append(sound.replace(sound[0], new_consonant))
            
    #extend vowels
    tones = "ˊˇˋ˙"
    sound_no_tone = sound.strip(tones)
    vowels = ['ㄛ','ㄜ','ㄝ','ㄢ','ㄣ','ㄡ','ㄦ','ㄟ','ㄤ','ㄥ']
    if sound_no_tone[-1] in vowels:
        new_vowel = vowels[(vowels.index(sound_no_tone[-1])+5)%len(vowels)]
        vowel_place = sound.index(sound_no_tone[-1])
        extended_sound.append(sound.replace(sound[vowel_place], new_vowel))
                
    return extended_sound

def extend_word_sound(sounds):
    extended_word_sound = []
    for sound in sounds:
        extended_word_sound += extend_one_sound(sound)
    return extended_word_sound
    
def search_sound(sentence, letter):
    #the Homonym of letter will latter be replaced with letter in sentence
    result = []
    letter_py = pinyin(letter, style=Style.BOPOMOFO, heteronym=True)
#    print(letter_py)
    sentence_py = pinyin(sentence, style=Style.BOPOMOFO, heteronym=True)
#    print(sentence_py)
    
    #iterate through diff sound of one word
    #letter_py[0]: letter_py is the pinyin of one letter, so only get 1st letter
    for sound in letter_py[0]: 
        #iterate through diff word in sentence
        for word_ix, word_py in enumerate(sentence_py):
            #word_py is the pinyin list of one word in sentence
#            print(sound)
#            print(word_py)
            
            extended_sound = extend_one_sound(sound)
                
            #sound's relatives in word_py    
            relative_sound = set(extended_sound).intersection(set(word_py))
            if relative_sound!=set():
                #word_ix : the index of word in sentence
                #sound_ix : the index of sound in a word
                relative_sound = list(relative_sound)[0]
                sound_ix = word_py.index(relative_sound)
                #meaning: letter's pinyin is same as the sound_ix of the word, 
                # which is the word_ix th word in sentence
                result.append((word_ix, sound_ix))
#    print(result)
    return result

def expressiondict_builder(expressions):
    expressiondict = {}
    
    for expression in expressions:
        multiple_sounds = pinyin(expression, style=Style.BOPOMOFO, heteronym=True)
        multiple_sounds = [extend_word_sound(sounds) for sounds in multiple_sounds]
        multiple_sounds = itertools.product(multiple_sounds[0], multiple_sounds[1], multiple_sounds[2])
        for ms in multiple_sounds:
            expressiondict[ms] = expression[2]
    
    return expressiondict

def surname_corrector(sentence):
    with open('expressiondict.pickle', 'rb') as handle:
        expressiondict = pickle.load(handle)
    main_clause, sub_clauses = re.split('\W+', sentence, maxsplit=1)
    final_main_clause = main_clause
    pysc = pinyin(sub_clauses, style=Style.BOPOMOFO, heteronym=True)
    pysc = (pysc[0][0], pysc[1][0], pysc[2][0])
    
    final_main_clause = final_main_clause.split('姓')[0] + '姓' + expressiondict[pysc]
    return final_main_clause
    
def sentence_corrector(sentence):
    main_clause, sub_clauses = re.split('\W+', sentence, maxsplit=1)
    final_main_clause = main_clause
    
    for sub_clause in re.split('\W+', sub_clauses):
#        print(sub_clause)
        if '是' in sub_clause:
            # delete 冬是 from 冬是东南西北的东
            sub_clause = sub_clause.split('是', maxsplit=1)[1]
        # example: 东南西北, keyword: 东
        example, keyword = sub_clause.split('的', maxsplit=1)
        word_ix, sound_ix = search_sound(example, keyword)[0]
    
        #example[word_ix] is the correct word
        correct_word = example[word_ix]
        
        #now find Homonym of the correct word in main_clause
#        print(main_clause, correct_word)
        word_ix, sound_ix = search_sound(main_clause, correct_word)[0]
        wrong_word = main_clause[word_ix]
#        print('{} will be replace to {}'.format(wrong_word, correct_word))
        final_main_clause = final_main_clause.replace(wrong_word, correct_word)
    
    return final_main_clause
        
sentences = [
        "冬地天蓝小区，冬是东南西北的东，地是天地的地，蓝是波澜不惊的澜",
        "心安镇,新旧的新,安全的安",
        "金泰路街道,北京的京,泰州的泰", #'金':jin1, '京':jing1
        "槿东花苑，锦绣前程的锦,东南西北的东",
        "一枚路,利益的益,梅花的梅",
        "政党，增加的增", #政:zheng, 增:zeng
        "测温，撤退的撤", #测:ce, 撤：che
        "数量，速度的速", #数:shu, 速：su
        ]

surname_sentences = [
        "我姓吴，口天吴",
        "我姓刘，文刀刘",
        "我姓张，弓长张",
        "我姓林，双木林",
        "我姓陈，耳东陈",
        "我姓李，木子李",
        "我姓章，立早章",
        "我姓吕，双口吕",
        "我姓王，三横王",
        "我姓胡，古月胡",
        "我姓杨，木易杨",
        "我姓许，言午许",
        "我姓姜，美女姜",
        "我姓嵩，山高嵩",
        "我姓松，木公松",
        "我姓江，水工江",
        "我姓姜，羊女姜",
        "我姓黄，草头黄",
        "我姓徐，双人徐",
        "我姓杜，木土杜",
        "我姓于，干钩于",
        "我姓孙，子小孙",
        ]

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

#expressiondict = expressiondict_builder(surname_expressions)
#with open('expressiondict.pickle', 'wb') as handle:
#    pickle.dump(expressiondict, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
#with open('expressiondict.pickle', 'rb') as handle:
#    expressiondict = pickle.load(handle)
    
#print(pinyin(sentence, style=Style.TONE3, heteronym=True))
#[['zhong1', 'zhong4'], ['xin1']]

for sentence in sentences:
    corrected_sentence = sentence_corrector(sentence)
    print('{} is now become {}'.format(sentence, corrected_sentence))
    
error_surname_examples = [
        "我姓许，双人徐",
        "我姓章，弓长张"
        ]

for sentence in error_surname_examples:
    corrected_sentence = surname_corrector(sentence)
    print('{} now becomes {}'.format(sentence, corrected_sentence))
