#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time
import pprint

def get_group_info(group_id):
	print "Getting data for group ", group_id
	group_info = vk.groups.getById(group_id=group_id, fields='members_count,description')
	count = group_info[0][u'members_count']
	return group_info, count

def check_if_group_exist(group_id):
	q = cur.execute('''SELECT * FROM Groups WHERE gid = ( ? )''', (group_id, ))
	if q.fetchone() is None:
		return False
	else:
		print "Group already in database"
		return True

def check_if_group_actual(group_id, group_info):
	cur.execute('''SELECT * FROM Groups WHERE gid = ( ? ) AND is_actual = 1''', (group_id, ))
	row = cur.fetchone()
	if group_info[0][u'name'] == row[4]:
		if group_info[0][u'screen_name'] == row[5]:
			if group_info[0][u'type'] == row[6]:
				if group_info[0][u'is_closed'] == row[7]:
					if group_info[0]['description'] == row[8]:
						print "Info for group is actual"
						return True
	
def add_group_to_db(group_info):
	cur.execute('''
		INSERT OR IGNORE INTO Groups (gid, is_actual, date_actual, 
			name, screen_name, type, is_closed, description) 
		VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )
		''', (group_info[0][u'gid'], "1", current_date, group_info[0][u'name'],  
				group_info[0][u'screen_name'], group_info[0][u'type'], 
				group_info[0][u'is_closed'], group_info[0]['description']))
	connection.commit()
	print "Add info about group %s into database" % group_id

def get_user_id(group_id, count):
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

def check_if_user_exist(user_id):
	q = cur.execute('''SELECT * FROM Users WHERE uid = ( ? )''', (user_id, ))
	if q.fetchone() is None:
		return False
	else:
		print "User %s already in database" % user_id
		return True		
	
def get_user_info(user_id):
	fields = "sex,bdate,city,country,personal,relatives,counters"
	user_info = vk.users.get(user_ids=user_id, fields=fields)
	time.sleep(0.2)
	count = user_info[0][u'counters'][u'friends']
	offset = 0
	friend_list = vk.friends.get(user_ids=user_id)
	time.sleep(0.2)
	return user_info, friend_list

def check_if_user_actual(user_id, user_info):
	(deactivated, bdate, political, religion, people_main, life_main, alchohol, 
		smoking, country, city) = handle_user_info(user_info)
	cur.execute('''SELECT * FROM Users WHERE uid = ( ? ) AND is_actual = 1''', (user_id, ))
	row = cur.fetchone()
	if user_info[0][u'first_name'] == row[5]:
		if user_info[0][u'last_name'] == row[6]:
			if bdate == row[7]:
				if user_info[0][u'sex'] == row[8]:
					if country == row[9]:
						if city == row[10]:
							if political == row[11]:
								if religion == row[12]:
									if people_main == row[13]:
										if life_main == row[14]:
											if alchohol == row[15]:
												if smoking == row[16]:
														print "Info for user is actual"
														return True	
	
def add_relatives(user_id):
	child_list = []
	try:
		print "Relatives for ", account[u'uid']
		relatives = account[u'relatives']
		for relative in relatives:
			add.relative()
		print child_list
	except:
		pass

def handle_user_info(user_info):
	try:
		deactivated = user_info[0][u'deactivated']
	except:
		deactivated = ""
	try:
		bdate = user_info[0][u'bdate']
	except:
		bdate = ""
	try:
		political = user_info[0][u'personal'][u'political']
	except:
		political = ""
	try:
		religion = user_info[0][u'personal'][u'religion']
	except:
		religion = ""
	try:
		people_main = user_info[0][u'personal'][u'people_main']
	except:
		people_main = ""
	try:
		life_main = user_info[0][u'personal'][u'life_main']
	except:
		life_main = ""
	try:
		alchohol = user_info[0][u'personal'][u'alchohol']
	except:
		alchohol = ""
	try:
		smoking = user_info[0][u'personal'][u'smoking']
	except:
		smoking = ""
	try:
		country = user_info[0][u'country']
	except:
		country = ""
	try:
		city = user_info[0]['city']
	except:
		city = ""
	return (deactivated, bdate, political, religion, people_main, life_main, 
		alchohol, smoking, country, city)
	
def add_user_to_db(user_info):			
	(deactivated, bdate, political, religion, people_main, life_main, alchohol, 
		smoking, country, city) = handle_user_info(user_info)
	cur.execute('''
		INSERT OR IGNORE INTO Users (uid, is_actual, date_actual, 
			deactivated, first_name, last_name, bdate, sex, country, city,
			political, religion, people_main, life_main, alchohol, smoking) 
		VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
		''', (user_info[0][u'uid'], "1", current_date, deactivated,
				user_info[0][u'first_name'], user_info[0][u'last_name'],  
				bdate, user_info[0][u'sex'], country, city,
				political, religion, people_main, life_main,
				alchohol, smoking))
	connection.commit()
	print "Add info about user %s into database" % group_id

	
#ПЕРЕПИСАТЬ!
#Надо запрашивать всех пользователей из базы и сравнивать через set(a).intersection(b),
#чтобы выделить новых друзей и друзей, которые стали неактуальны is_actual = 0
def add_friends_list(user_id, friend_list):
	for friend in friend_list:
		q = cur.execute('''SELECT * FROM Users_friends WHERE user_id = ( ? ) 
			and friend_id = ( ? )''', (user_id, friend))
		if q.fetchone() is None:
			cur.execute('''INSERT OR IGNORE INTO Users_friends (user_id, friend_id,
				is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
				''', (user_id, friend, "1", current_date, "friend"))
			connection.commit()
		else:
			continue

def add_group_members(group id, id_list):
	for id in id_list:
		q = cur.execute('''SELECT * FROM Groups_members WHERE group_id = ( ? ) 
			and user_id = ( ? )''', (group_id, id))
		if q.fetchone() is None:
			cur.execute('''INSERT OR IGNORE INTO Groups_members (user_id, friend_id,
				is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
				''', (user_id, friend, "1", current_date, "friend"))
			connection.commit()
		else:
			continue		
#КОНЕЦ того, что надо переписывать	
			
group_id = '38532412' #vk.com/privivkanet
current_date = time.strftime("%d %b %Y",time.gmtime())

connection = sqlite3.connect('vk_vaccination.db')
cur = connection.cursor()

print "Connected to database\n * * * \n"

token = open("token.txt").read()
vk = vkontakte.API(token=token)

group_info, count = get_group_info(group_id)

#add info about start group to database
if check_if_group_exist(group_id) is False:
	add_group_to_db(group_info)
else:
	if check_if_group_actual(group_id, group_info) is not True:
		cur.execute('''UPDATE Groups SET is_actual = 0 WHERE gid = ( ? ) 
			and is_actual = 1''', (group_id, ))
		add_group_to_db(group_info)
		connection.commit()

#add to database list of start group's members and their info
id_list = get_user_id(group_id, count)
x = 1
for user_id in id_list[0:2]:
	print "Getting user info for %s of %s" % (x, count)
	user_info, friend_list = get_user_info(user_id)
	add_friends_list(user_id, friend_list)
	if check_if_user_exist(user_id) is False:
		add_user_to_db(user_info)
	else: 
		if check_if_user_actual(user_id, user_info) is not True:
			cur.execute('''UPDATE Users SET is_actual = 0 WHERE uid = ( ? ) 
				and is_actual = 1''', (user_id, ))
			add_user_to_db(user_info)
			connection.commit()
	x += 1


