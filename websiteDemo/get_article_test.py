import get_article


#url = 'https://www.cna.com.tw/news/firstnews/201807090015.aspx'
url = 'https://www.cna.com.tw/postwrite/Detail/218167.aspx#.XDf3SnUzZ3k'
article = get_article.get_news_article(url)
print(article)
