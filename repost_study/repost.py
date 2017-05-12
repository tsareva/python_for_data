#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import messages
import create_token as ct
import time, sqlite3, vkontakte, time
import pandas as pd

def get_sum(data):
	sum = 0
	for row in data:
		if isinstance(row[6], basestring) is False:
			sum+=row[6]
	return sum

def get_reposter_list(data)	:
	reposter_list = []
	for row in data:
		if row[6] > 0:
			#repost = post id, user id
			repost = (row[2], row[3])
			if repost not in reposter_list:
				reposter_list.append(repost)
	return reposter_list

def get_server_time():
	token = open("files/token.txt").read()
	vk = vkontakte.API(token=token)
	server_time = vk.getServerTime()
	print "Time now: ", time.ctime(int(server_time))
	
try:
	get_server_time()
except vkontakte.api.VKError as error:
	if error.code == 5:
		ct.create_token()
		get_server_time()
		quit()
	else:
		print error
		quit()
	
group_id = raw_input("Enter id (should be with - for groups): ") 
# should be with '-' for groups
message_id = raw_input("Enter message id: ") 

fieldnames = ["unixdate", "m_id", "from_user", "source", "likes_count", "repost_count", "copy_text"]

data = messages.get_all_reposts(group_id, message_id)
result_filename = (raw_input("Enter result database name: "))+ ".db"

reposter_list = get_reposter_list(data)
y = get_sum(data)
print "There are % reposts more" % y

while y > 0:
	rfr_data = []
	for reposter in reposter_list:
		time.sleep(0.2)
		print "Look for reposts from ", reposter[1]
		repost_data = messages.get_all_reposts(reposter[1], reposter[0]) 
		if len(repost_data) > 0:
			for row in repost_data:
				row[4] = reposter[1]
		rfr_data+=repost_data
	data += rfr_data
	y = get_sum(rfr_data)
	print "There are % reposts more" % y
	reposter_list = get_reposter_list(rfr_data)
	
df = pd.DataFrame(data, columns = fieldnames)
subset = fieldnames [0:4] + fieldnames [7:]
result = df.drop_duplicates(subset, keep='last')

con = sqlite3.connect(result_filename)

result.to_sql('Reposts', con)

