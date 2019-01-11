# -*- coding: utf-8 -*- 
import json
import jieba
import os.path
import numpy as np


#jieba.set_dictionary('dict.txt.big')
stops =[]
stop_words = [' ', '\n', '（', '）', '。', '「', '」', '『', '』', '：', ':', '[影]', '？', '！', '；', '──', '……', '—', '〔', '〕']
for word in stop_words:
    stops.append(word)

def tag_replace(split):
    keyword_date = ['年', '月', '日', '/']
    keyword_url = ['.', '/', '-', '_', '+', '=', '@', '?', '&']
    i = 0

    def isNumber(word):
        try:
            float(word)
        except ValueError:
            return False
        return True

    while i < len(split):
        if isNumber(split[i]):
            j = i
            while j + 1 < len(split) and (split[j + 1] in keyword_date or split[j + 1] is '/'):
                j += 2
                if isNumber(split[i]):
                    continue
                else:
                    break
            if j == i:
                split[i] = 'TAG_NUMBER'
            else:
                split[i] = 'TAG_DATE'
                del split[i+1:j]
        if '%'in split[i]:
            split[i] = 'TAG_NUMBER'
        if 'http' in split[i]:
            j = i + 1
            while j + 1 < len(split) and split[j + 1] in keyword_url:
                j += 2
            split[i] = 'TAG_URL'
            del split[i+1:j+1]
        i += 1
    if split:
        split.pop()

def splitWords(input_sequence):
	article = [t for t in jieba.cut(input_sequence) if t not in stops]
	tag_replace(article)
	#print(article)
	blank = " "
	#print(blank.join(article))
	return blank.join(article)
'''
input_sequence = "我好帥工程師"
article = [t for t in jieba.cut(input_sequence) if t not in stops]
tag_replace(article)
print(article)
blank = " "
print(blank.join(article))
'''
