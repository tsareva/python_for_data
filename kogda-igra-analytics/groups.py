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
	if len(data) > 0:
		print "Saving results..."
		result_file = codecs.open(filename, "wb", "utf-8-sig")
		writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow(fieldnames)
		for row in data:
			writer.writerow(row)
		print "Results were saved in ", filename
		result_file.close()
	else:
		print "No data to be saved"

def create_group_info(group):
	row =[]
	row.append(group[u'gid'])
	row.append(group[u'screen_name'])
	row.append(group[u'type'])	
	row.append(group[u'name'])
	row.append(group[u'description'])
	return row

def get_group_list(user):
	print "Creating group list for user #", user
	groups = vk.groups.get(user_id=user, extended = 1, fields = "description")
	return groups

def getMembers(group, offset, users):
	user_list = vk.groups.getMembers(group_id=group[u'gid'], offset=offset)
	time.sleep(0.2)
	for user in user_list[u'users']:
		users.append(user)	
	count = user_list[u'count']
	return count
	
def get_members_list(group):	
	offset = 0
	users = []
	count = getMembers(group, offset, users)
	while (count > len(users)) and offset < 3000:
		offset += 1000
		getMembers(group, offset, users)
	return count, users
	
def append_group_info(group):
	row = create_group_info(group)
	count, users = get_members_list(group)
	row.append(count)
	row.append(users)
	if row not in data:
		data.append(row)
		group_count[group[u'gid']] = 1
	else:
		group_count[group[u'gid']] += 1
		
token = open("token.txt").read()
vk = vkontakte.API(token=token)
		
profiles = vk.groups.getMembers(group_id='122564943', count = 2)
data = []
#get all user ids for group
group_count = dict()
no_data = []
for user in profiles[u'users']:
	try:
		groups = get_group_list(user)
		for group in groups[1:]:
			append_group_info(group)
	except:
		no_data.append(user)
		pass
print "Groups were counted"

if len(no_data) == 0:
	print "For all users data were get succesfully"
else:
	print "Can't get data for: %d percents of members" % (len(no_data)/len(profiles[u'users'])*100)
	pprint.pprint(no_data)

for key, value in group_count.iteritems():
	for line in data:
		if line[0] == key:
			line.append(value)

fieldnames = ["ID", "Screen name", "Type", "Name", "Description", "Count of group members","Members IDs","Count with dict"]
write_to_result('groups_info.csv', data, fieldnames)	
