#-*-coding:utf-8 -*-
import web_news_splits
import sys
sys.path.append('/home/team6/ArticleTitleGenerator/model')
import predict_website
import random
from flask import Flask,request
from flask import jsonify
import utils
import get_article

app = Flask(__name__,static_url_path='',root_path='/home/team6/final_demo_website')    
@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/Ajax')
def Ajax():
	url = request.args.get('url')
	article = get_article.get_news_article(url)
	cut_sequence = web_news_splits.splitWords(article)
	#cut_content = utils.cutToWord(content)
	#output = predict_website.decode(cut_content)
	output = predict_website.decode(cut_sequence)
	result = {'predict':output,'article':article}
	return jsonify(result)

@app.route('/dataFromAjax')
def dataFromAjax():
	test = request.args.get('mode')
	#x,y = utils.getRandomXY(0,95,0,91)
	#print(x,y)
	result = {'x':55,'y':72}
	#result = ['aa',5]
	return jsonify(result)




if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0',port=8892,debug=False)
