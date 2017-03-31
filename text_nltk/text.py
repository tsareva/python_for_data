#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv
import nltk
from nltk.corpus import stopwords
import pymorphy2
from stop_words import get_stop_words

def write_to_result (filename, data, fieldnames):
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	result_file.close()

def delete_url(text):
	if text.find("http") is not -1:
		i = text.index("http")
		try:
			j = text[i:].index(" ")
			new_text = text.replace(text[i:j], "")
			return new_text
		except:
			new_text = text.replace(text[i:], "")
			return new_text
	else:
		return text
	
with codecs.open("19732513-post.txt", 'r', 'utf-8-sig') as file:
	opened_file = file.read().split("\n")
	fieldnames = opened_file[0].split("\t")
	data = []
	for row in opened_file[1:]:
		data.append(row.split("\t"))

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
morph = pymorphy2.MorphAnalyzer()

stopWords = stopwords.words('russian')
stop_words = get_stop_words('russian')
for word in stop_words:
	if word not in stopWords:
		stopWords.append(word)
with codecs.open("extra_stopwords.txt", 'r', 'utf-8-sig') as file:
	opened_file = file.read().split("\n")
	for stopword in opened_file:
		if stopword not in stopWords:
			stopWords.append(stopword)
stopWords = set(stopWords)


WordsSet = []
n = 0
l = len(data)
while n < l:
	if len(data[n]) == 11:
		m = delete_url(data[n][10])
		words = tokenizer.tokenize(m)
		time = data[n][4]
		for w in words:
			try:
				int(w)
				continue
			except:
				if w.lower() not in stopWords:
					line = []
					line.append(time)
					line.append(morph.parse(w)[0].normal_form)
					if line not in WordsSet:
						WordsSet.append(line)
	n+=1
	print "%s of %s messages done" % (n, l)

fieldnames = ["date", "word"]
	
write_to_result ('r.csv', WordsSet, fieldnames)
