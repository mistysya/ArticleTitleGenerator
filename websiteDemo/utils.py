# -*- coding:utf8 -*-
import jieba
import random

def getRandomXY(a,b,c,d):
	x = random.randint(a,b)
	y = random.randint(c,d) 

	return x,y
def cutToWord(input_article):
	seg_list = jieba.cut(input_article,cut_all=False)
	result = []
	for i in seg_list:	
		if not i.isdigit():
			result.append(i)
		else:
			result.append("TAG_NUMBER")
	
	blank=" "
	return blank.join(result)
