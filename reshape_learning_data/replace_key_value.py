#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv

writef = open('recode_result.sps','w')

def read_csv_file(filename):
	with codecs.open(filename, 'r', 'utf-8-sig') as file:
		print "Getting data from... ", filename
		opened_file = csv.reader(file, delimiter=';')
		fieldnames = next(opened_file) 
		data = []
		for row in opened_file:
			data.append(row)
	return data

data = read_csv_file('faculties.csv')
faculties = dict()

for row in data:
	value = row[1] + " (" + row[2] + ")"
	faculties[row[0]] = value 
	
with open('result.sps', 'r') as f:
	content = f.readlines()

for line in content:
	line = line.replace(".sps", "")
	for key, value in faculties.iteritems():
		if line.find(key) is not -1:
			line = line.replace(key, value)
	writef.write(line)