from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
import time
import datetime
import sys
import os

# https://www.cna.com.tw/news/aopl/201611210461.aspx
DATA_FILENAME = 'news_cna'
base_url = 'https://www.cna.com.tw/news/aopl/'
year = 2016
month = 1  # str(1).zfill(2)
day = 1  # str(1).zfill(2)
news_number = 1  # str(1).zfill(4)


def get_web(url):
    global feed
    try:
        html = urlopen(url)
    except:
        return False
    bsObj = BeautifulSoup(html, "lxml")
    content = bsObj.find("article").find("div", {"class": "centralContent"})
    if content is None:
        return False
    date = str(year) + '/' + str(month).zfill(2) + '/' + str(day).zfill(2)
    # print('------date------')
    # print(date)
    number = str(news_number).zfill(4)
    print(number)
    title = content.find("h1").get_text()
    print('------title------')
    print(title)
    article = content.find("div", {"class": "paragraph"}).get_text()
    summary = content.find("div", {"class": "paragraph"}).find("p").get_text()
    # print('------summary------')
    # print(summary)
    # print('------article------')
    # print(article)
    # print('------news------')
    news = {'date': date, 'number': number, 'title': title, 'summary': summary, 'article': article}
    # print(news)
    feed.append(news)
    return True


def initial_date(_year, _month, _day):
    global year, month, day, news_number
    year = _year
    month = _month
    day = _day
    news_number = 1


if len(sys.argv) != 7:
    print("Please enter correct parameter format")
    print("Start date: YYYY MM DD   End date: YYYY MM DD")
    print("news_scraper.py 20XX XX XX 20XX XX XX")
    sys.exit(0)
feed = []
initial_date(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
scrap_date = datetime.date(year, month, day)
end_date = datetime.date(int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
# end_date = datetime.date.today()
while (scrap_date < end_date):
    print(str(scrap_date.strftime("%Y-%m-%d")))
    reconnect_count = 0
    filename = DATA_FILENAME + '_' + str(scrap_date.year) + '_' + str(scrap_date.month) + '.json'
    if os.path.isfile(filename):
        pass
    else:
        with open(filename, mode='w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)
    with open(filename, mode='r') as feeds:
        # entry = {'name': args.name, 'url': args.url}
        feeds = json.load(feeds)

    for num in range(600):
        if get_web(base_url + str(scrap_date.year) + str(scrap_date.month).zfill(2) + str(scrap_date.day).zfill(2) + str(news_number).zfill(4) + '.aspx') is False:
            print("Connect ERROR!", str(reconnect_count))
            reconnect_count += 1
            if reconnect_count > 15:
                print("Reconnet > 10 times. Shutdown the loop")
                break
        else:
            reconnect_count = 0
        news_number += 1
        time.sleep(2)
    feeds.extend(feed)
    with open(filename, mode='w', encoding='utf-8') as feedsjson:
        json.dump(feeds, feedsjson, ensure_ascii=False, indent=4, separators=(',', ': '))

    scrap_date += datetime.timedelta(days=1)
    feed = []
    year = scrap_date.year
    month = scrap_date.month
    day = scrap_date.day
    news_number = 1
    pass
