#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys, socket, ssl
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time

token = open("files/token.txt").read()
vk = vkontakte.API(token=token)

def get_friends(user_id):
	friends = []
	try:
		f_list = vk.friends.get(user_id=user_id)
		for friend in f_list:
			connection = []
			connection.append(user_id)
			connection.append(friend)
			friends.append(connection)
			time.sleep(0.2)
		return friends
	except vkontakte.api.VKError as error:
		if error.code == 18:
			return friends
			pass
		else: 
			print error
			pass
