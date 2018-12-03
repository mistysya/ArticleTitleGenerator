import json
import jieba
import os.path
import numpy as np


jieba.set_dictionary('dict.txt.big')
# with open('stops.txt', 'r', encoding='utf8') as f:
#    stops = f.read().split('\n')
stops =[]
# stop_words = [' ', '\n', '（', '）', '，', '。', '「', '」', '『', '』', '：', '、', '"', ':', '[影]', '？', '！', '；', '──', '……', '—', '〔', '〕']
stop_words = [' ', '\n', '（', '）', '。', '「', '」', '『', '』', '：', ':', '[影]', '？', '！', '；', '──', '……', '—', '〔', '〕']
for word in stop_words:
    stops.append(word)
# print([t for t in jieba.cut('下雨天留客天留我不留')])

'''
print('===================')
print(data[0]['title'])
print([t for t in jieba.cut(data[0]['title'])])
print('===================')
print(data[0]['summary'])
print([t for t in jieba.cut(data[0]['summary'])])
print('===================')
print(data[0]['article'])
print([t for t in jieba.cut(data[0]['article'])])
print('===================')
'''

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


total = 0
years = [2016, 2017, 2018]
for year in years:
    for i in range(12):
        # templet setting
        if year is '2018' and i+1 is 3:
            continue
        # templet setting
        file_path = 'news_cna_' + str(year) + '_' + str(i+1) + '.json'
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf8') as f:
                data = json.load(f)
            print(year, i+1, len(data))
            total += len(data)
            for news in data:
                title = [t for t in jieba.cut(news['title']) if t not in stops]
                tag_replace(title)
                article = [t for t in jieba.cut(news['article']) if t not in stops]
                tag_replace(article)
                with open('title_output.txt', 'a', encoding='utf8') as f:
                    f.write(" ".join(title))
                    f.write('\n')
                with open('article_output.txt', 'a', encoding='utf8') as f:
                    f.write(" ".join(article))
                    f.write('\n')
print(total)

'''
new = {
    "date": "2016/11/24",
    "number": "0204",
    "title": "（中央社記者王承中台北24日電） 2018年2月2日 日日 2018/2/4 13.2% 其他地區則在27至29度 只有10.3公里 高達3公尺 清晨5時55分 11月28日 需要600萬至700萬美元 消防員免捕蜂捉蛇 消防署訂兩年計畫 http://goo.gl/hE5Oct/opencv-cpp_python.html",
    "summary": "（中央社記者王承中台北24日電）內政部長葉俊榮今表示，消防署最近跟農政單位協商，提出兩年計畫，盼銜接捕蜂捉蛇、抓貓抓狗的業務。消防署長陳文龍指出，希望後年底前各地農政單位建立24小時受理處理機制。",
    "article": "（中央社記者王承中台北24日電）內政部長葉俊榮今表示，消防署最近跟農政單位協商，提出兩年計畫，盼銜接捕蜂捉蛇、抓貓抓狗的業務。消防署長陳文龍指出，希望後年底前各地農政單位建立24小時受理處理機制。立法院內政委員今天審查內政部消防署預算，葉俊榮、陳文龍受邀列席。對於捕蜂捉蛇、抓貓抓狗等救援工作，已使基層消防員承受過多業務，有立委提案欲凍結消防署預算，盼盡速讓消防員回歸救災救護本務。據查，消防隊近3年處理業務比例中火災類佔4.8%，緊急救護類佔81.2%，其他類(包含捕風捉蛇、動物救援等)佔13.2%，災害搶救類佔0.7%。受理其他類案件高於火災類，且又以捕蜂(26.4%)、捉蛇(33%)為最大宗。對此，葉俊榮表示，消防署最近很努力在跟農政單位協商，希望能夠把捕蜂捉蛇、抓貓抓狗的業務做合理的銜接 ，因此有提出兩年計畫，讓農政、動保團體建立處理的量能。葉俊榮指出，今年9月在跨部會議中，已決議將「各部會協助動物保護政策規劃分工表」中「動物救援機制(犬貓)」主辦部會中，將消防署刪除。針對兩年計畫，陳文龍在會後表示，捕蜂捉蛇、抓貓抓狗等業務，消防隊不是專業，有些動物如鱷魚，消防員沒有辦法處理，這是動物保護的問題，希望在兩年內、後年年底前各地農政單位可委託第三機構接手，建立24小時的受理處理機制。陳文龍指出，民眾報案還是可以透過119，但是當電話進到119後，會再轉給受委託的第三單位做專業的處理。目前犬貓的問題，大部分的縣市已由農政單位處理，全國只有雲林縣等6縣市是全由消防局在做。1041124"
}
split = [t for t in jieba.cut(new['title']) if t not in stops]
print('===================')
print(new['title'])
print(split)
print('===================')
tag_replace(split)
print(split)
with open('output.txt', 'a', encoding='utf8') as f:
    f.write(" ".join(split))
    f.write('\n')
print('===================')
#print(data[0]['summary'])
#print([t for t in jieba.cut(new['summary']) if t not in stops])
print('===================')
#print(data[0]['article'])
#print([t for t in jieba.cut(new['article']) if t not in stops])
print('===================')

'''