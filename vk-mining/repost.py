#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import group
import messages
import time, sqlite3, vkontakte
import codecs, csv

def write_to_result (filename, data, fieldnames):
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	result_file.close()

def get_r_count(data):
	r_count = 0
	for line in data:
		r_count += line[6]
	return r_count

n_repost = messages.get_n_repost("-19732513", "235977")	
print "There are %s reposts of original message" % n_repost

fieldnames = ["unixdate", "date", "m_id", "from_user", "source", "likes count", "repost count", "copy_text", "reposter type", "depth"]
data = []
offset=0
while len(data)-2 < 455:
	reposts = messages.get_reposts("-19732513", "235977", offset)
	get_data = messages.get_repost_data(reposts)
	data+=get_data
	print "Get %s of %s reposts" % (len(data), n_repost)
	offset+=150


write_to_result("r.csv", data, fieldnames)