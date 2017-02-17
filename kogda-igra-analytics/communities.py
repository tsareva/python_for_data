#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv

import urllib, vkontakte, pprint
import time

def get_profiles_from_group(group_id):
	offset = 0
	id_list = []
	list = vk.groups.getMembers(group_id=group_id)
	user_info = get_profile(list[u'users'])
	time.sleep(0.2)
	count = list[u'count']
	print count, " users are in this group"
	for user in list[u'users']:
		id_list.append(user)
	while (count > len(id_list)):
		offset += 1000
		list = vk.groups.getMembers(group_id=group_id, offset=offset)
		user_info_1000 = get_profile(list[u'users'])
		user_info += user_info_1000
		time.sleep(0.2)
		for user in list[u'users']:
			id_list.append(user)	
	return id_list, user_info

def create_user_info(user):
	row = []
	row.append(user[u'uid'])
	row.append(user[u'first_name'])
	row.append(user[u'last_name'])
	row.append(user[u'sex'])
	try:
		row.append(user[u'bdate'])
	except:
		row.append("")
	try:
		row.append(user[u'city'])
	except:
		row.append("")	
	try:	
		row.append(user[u'country'])
	except:
		row.append("")
	return row
	
	
def get_profile(user_ids):
	user_info = []
	fields = "sex, bdate, city, country"
	profiles = vk.users.get(user_ids=user_ids, fields=fields)
	for user in profiles:
		row = create_user_info(user)
		user_info.append(row)
	return user_info

def get_personal(id_list):
	personal_list = []
	n = 1
	for id in id_list:
		print n, " of ", len(id_list)
		line = []
		line.append(id)
		try:
			profile = vk.users.get(user_ids=id, fields="personal")
			personal = profile[0][u'personal']
			row = create_personal_info(personal)
			line += row
			time.sleep(0.2)
		except:
			x = 0
			while x < 2:
				line.append("")
				x+=1
			pass
		personal_list.append(line)
		n+=1
	return personal_list

def create_personal_info(personal):
	row = []
	try:
		row.append(personal[u'alcohol'])
	except:
		row.append("")
	try:
		row.append(personal[u'smoking'])
	except:
		row.append("")	
	return row
	
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
		
token = open("token.txt").read()
vk = vkontakte.API(token=token)

id_list, profiles = get_profiles_from_group('109407511')
personal_data = get_personal(id_list)

for profile in profiles:
	for line in personal_data:
		if line[0] == profile[0]:
			for element in line[1:]:
				profile.append(element)


fieldnames = ["User ID", "First name", "Last name", "sex", "bdate", "city", "country", "alchohol", "smoking"]
write_to_result("user_info.csv", profiles, fieldnames)
