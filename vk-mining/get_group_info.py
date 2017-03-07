#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time
import pprint

def get_group_info(group_id):
	x = 1
	while True:
		try:
			print "Getting data for group ", group_id
			group_info = vk.groups.getById(group_id=group_id, fields='members_count,description,contacts,links')
			count = group_info[0][u'members_count']
			return group_info, count
		except:
			print "Can't create connection for %s time. Trying again..." % x
			time.sleep(1)
			x += 1
		
