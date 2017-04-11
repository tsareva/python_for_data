#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import group
import messages
import time, sqlite3, vkontakte
import work_with_csv
import pprint

def get_r_count(data):
	r_count = 0
	for line in data:
		r_count += line[6]
	return r_count

id = raw_input("Enter id (hould be with - for groups)") # should be with - for groups
message_id = raw_input("Enter message id") 

n_repost = 0 #messages.get_n_repost(id, message_id)	
print "There are %s reposts of original message" % n_repost

fieldnames = ["unixdate", "date", "m_id", "from_user", "source", "likes count", "repost count", "copy_text", "reposter type"]
data = []
offset=0
get_data = ["Start with it"]
while len(get_data) <> 0:
	reposts = messages.get_reposts(id, message_id, offset)
	get_data = messages.get_repost_data(reposts)
	for line in get_data:
		if line not in data:
			data.append(line)
	print "Get %s of %s reposts" % (len(data), n_repost)
	offset+=150



result_filename = str(id)+"-message"+str(message_id)+"-reposts.csv"
work_with_csv.write_to_result(result_filename, data, fieldnames)