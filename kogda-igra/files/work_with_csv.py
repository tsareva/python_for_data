#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv

def read_csv_file(filename):
	with codecs.open(filename, 'r', 'utf-8-sig') as file:
		print "Getting data from... ", filename
		opened_file = csv.reader(file, delimiter=',')
		fieldnames = next(opened_file) 
		data = []
		for row in opened_file:
			data.append(row)
	return data, fieldnames

def write_to_result (filename, data, fieldnames):
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	print "Results were saved into", filename
	result_file.close()