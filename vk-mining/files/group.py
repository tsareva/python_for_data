#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time

token = open("files/token.txt").read()
vk = vkontakte.API(token=token)

def get_info(group_id):
	x = 1
	while True:
		try:
			print "Getting data for group ", group_id
			fields='members_count,description,contacts,links'
			all_group_info = vk.groups.getById(group_ids=group_id, fields=fields)
			group_info = create_group_info_dict(all_group_info)
			count = all_group_info[0].get(u'members_count', None)
			contacts = all_group_info[0].get(u'contacts', None)
			links = all_group_info[0].get(u'links', None)
			return group_info, count, contacts, links
		except:
			continue

def create_group_info_dict(all_group_info):
	group_info = dict()
	group_info[u'gid'] = all_group_info[0].get(u'gid', "")	
	group_info[u'name'] = all_group_info[0].get(u'name', "")
	group_info[u'screen_name'] = all_group_info[0].get(u'screen_name', "")	
	group_info[u'type'] = all_group_info[0].get(u'type', "")	
	group_info[u'is_closed'] = all_group_info[0].get(u'is_closed', "")		
	group_info[u'description'] = all_group_info[0].get(u'description', "")
	return group_info
	
def get_members_ids(group_id, count):
	offset = 0
	id_list = []
	while (count > len(id_list)):
		try:
			list = vk.groups.getMembers(group_id=group_id, offset=offset)
			id_list += list[u'users']
			print "Getting member list: %s of %s done" % (len(id_list), count)
			offset += 1000
			time.sleep(0.2)
		except:
			time.sleep(0.2)
			continue
	return id_list
	
