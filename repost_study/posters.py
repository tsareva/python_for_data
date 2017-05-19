#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import group
import user_info as ui
import create_token as ct
import time, sqlite3, vkontakte, time
import pandas as pd

try:
	ct.get_server_time()
except vkontakte.api.VKError as error:
	if error.code == 5:
		ct.create_token()
		ct.get_server_time()
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

print "There are %s users" % len(users)

all_friends = []
n = 1
for user_id in users:
	print "Getting friends for %s user of %s" % (n, len(users))
	friends = ui.get_friends(user_id)
	all_friends += friends
	n+=1

fieldnames = ['user_id', 'friend_id']
df = pd.DataFrame(all_friends, columns = fieldnames)
c.execute('DROP TABLE Friends IF EXIST')
result.to_sql('Friends', con)

c.execute('SELECT Reposts.from_user FROM Reposts WHERE Reposts.from_user < 0')
groups = []
for item in c.fetchall(): groups.append(item[0])