from urllib2 import urlopen
from bs4 import BeautifulSoup


def get_news_article(url):
    base_url = 'https://www.cna.com.tw/news/'
    if base_url not in url:
        return None
    else:
        try:
            html = urlopen(url)
        except Exception as e:
            print("URL open fail. Please check the url or network status.")
            return None
        bsObj = BeautifulSoup(html, "lxml")
        content = bsObj.find("article").find("div", {"class": "centralContent"})
        if content is None:
            return None
        article = content.find("div", {"class": "paragraph"}).get_text()
        return article
