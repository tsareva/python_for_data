#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time
import pprint

def get_user_info(user_id):
	print "Getting user info ..."
	x = 1
	while True:
		try:
			fields = "sex,bdate,city,country,personal,relatives,counters"
			user_info = vk.users.get(user_ids=user_id, fields=fields)
			time.sleep(0.2)
			try:
				friend_list = vk.friends.get(user_id=user_id)
				time.sleep(0.2)
			except:
				friend_list = []
			try:
				group_list = vk.groups.get(user_id=user_id)
				time.sleep(0.2)
			except:
				group_list = []
			return user_info, friend_list, group_list
		except:
			print "Can't create connection for %s time. Trying again..." % x
			time.sleep(1)
			x += 1

			
user_id = "147063"
token = open("token.txt").read()
vk = vkontakte.API(token=token)

user_info, friend_list, group_list = get_user_info(user_id)
print user_info, friend_list, group_list