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
	
database = (raw_input("Enter result database name: "))+ ".db"

con = sqlite3.connect(database)
c = con.cursor()

c.execute('SELECT Reposts.from_user FROM Reposts WHERE Reposts.from_user > 0')
users = []
for item in c.fetchall(): users.append(item[0])

c.execute('SELECT Reposts.from_user FROM Reposts WHERE Reposts.from_user < 0')
groups = []
for item in c.fetchall(): groups.append(item[0])