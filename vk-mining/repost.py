#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import group
import messages
import time, sqlite3, vkontakte, time
import work_with_csv
import pprint

group_id = "-19732513" #raw_input("Enter id (hould be with - for groups): ") # should be with - for groups
message_id = "235977"#raw_input("Enter message id: ") 

fieldnames = ["unixdate", "date", "m_id", "from_user", "source", "likes count", "repost count", "copy_text", "reposter type"]

data = messages.get_all_reposts(group_id, message_id)

reposter_list = []
for row in data:
	if row[6] > 0:
		#repost = post id, user id
		repost = (row[2], row[3])
		if repost not in reposter_list:
			reposter_list.append(repost)
		
rfr_data = []		
for reposter in reposter_list:
	time.sleep(0.2)
	print "Look for reposts from ", reposter[1]
	repost_data = messages.get_all_reposts(reposter[1], reposter[0]) 
	if len(repost_data) > 0:
		row[4] = reposter[1]
	rfr_data+=repost_data

not_found = []
for line in rfr_data:
	for row in data:
		if str(row[2]) == str(line[2]) and str(row[3]) == str(line[3]):
			row[4] = str(line[4])
		else: 
			if line not in not_found:
				not_found.append(line)


result_filename = str(group_id)+"-message"+str(message_id)+"-reposts.csv"		
work_with_csv.write_to_result(result_filename, data, fieldnames)
work_with_csv.write_to_result('not_found.csv', not_found, fieldnames)