#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv

import urllib, vkontakte, pprint
import time

def create_fieldnames(dictionary):
	dict = user_info[0]
	fieldnames = []
	for key, value in dict.iteritems():
		fieldnames.append(key)
	return fieldnames
	
def write_to_result(filename, data, fieldnames):
	print "Saving results..."
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	print "Results were saved in ", filename
	result_file.close()

def create_group_info(group):
	row =[]
	row.append(group[u'gid'])
	row.append(group[u'screen_name'])
	row.append(group[u'type'])	
	row.append(group[u'name'])
	row.append(group[u'description'])
	return row
	
token = open("token.txt").read()
	
vk = vkontakte.API(token=token)

profiles = vk.groups.getMembers(group_id='122564943')

data = []

#get all user ids for group
user_ids = ''
group_count = dict()
for user in profiles[u'users']:
	user_ids += (str(user) + ", ")
	print "Creating group list for user #", user
	groups = vk.groups.get(user_id=user, extended = 1, fields = "description")
	for group in groups[1:]:
		row = create_group_info(group)
		if row not in data:
			data.append(row)
			group_count[group[u'gid']] = 1
		else:
			group_count[group[u'gid']] += 1
	time.sleep(0.2)
print "Groups were counted"
	

for key, value in group_count.iteritems():
	for line in data:
		if line[0] == key:
			line.append(value)

#		else:
#			print "Can't find id %s in data" 

fieldnames = ["ID", "Screen name", "Type", "Name", "Description","Count"]
write_to_result('results.csv', data, fieldnames)	