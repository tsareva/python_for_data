import csv, codecs
from collections import Counter

with codecs.open("example.txt","r","utf-8-sig") as file:
	text = file.read()
with open("stoplist.txt","r") as stopfile:
	stopfile = stopfile.read()
	stoplist = stopfile.split("\n")
for i in stoplist:
	text = text.replace(i, ' ')
text = text.lower()
text = text.split(" ")
print text

words = []

for i in text:
	if (i.strip() != ""):
		words.append(i.strip())
count = Counter()
for word in words:
	count[word] +=1

count = dict(count)
print count

with codecs.open("counted_data.csv","wb") as for_tableau:
	fieldnames = ['words', 'words_number']
	writer = csv.DictWriter(for_tableau, fieldnames=fieldnames)
	
	writer.writeheader()
	for k,v in count.iteritems():
		writer.writerow({'words': k.encode('utf-8'), 'words_number': v})