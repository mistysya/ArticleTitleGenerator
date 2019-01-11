# -*- coding:utf8 -*-
import jieba

seg_list = jieba.cut("工程師3帥哥a",cut_all=False)
result = []
for i in seg_list:	
	if not i.isdigit():
		result.append(i)
	else:
		result.append("TAG_NUMBER")
	
blank=" "
print(blank.join(result))


