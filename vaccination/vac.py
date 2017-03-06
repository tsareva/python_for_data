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
	print "Check if user exist in database"
	q = cur.execute('''SELECT * FROM Users WHERE uid = ( ? )''', (user_id, ))
	if q.fetchone() is None:
		return False
	else:
		return True		
	
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
			
def check_if_user_actual(user_id, user_info):
	print "Check actuality of user info in database"
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
														return True	
								
def add_relatives(user_info):
	print "Looking for relatives..."
	relatives = user_info[0].get(u'relatives', None)
	if relatives is not None:
		for relative in relatives:
			name = relative.get(u'name', "")
			cur.execute('''INSERT OR IGNORE INTO Relatives (user_id, relative_id, is_actual, date_actual, type, name)
				VALUES ( ?, ?, ?, ?, ?, ? )''', (user_info[0][u'uid'], relative[u'uid'], "1", current_date,	relative[u'type'], name))
		
def handle_user_info(user_info):
	deactivated = user_info[0].get(u'deactivated', "")
	bdate = user_info[0].get(u'bdate', "")
	personal = user_info[0].get(u'resonal', None)
	country = user_info[0].get(u'country', "")
	city = user_info[0].get(u'city', "")
	if personal is None:
		political = ""
		religion = ""
		people_main  = ""
		life_main = ""
		alchohol = ""
		smoking = ""
	else:
		political = personal.get(u'political', "")
		religion = personal.get(u'religion', "")
		people_main = personal.get(u'people_main', "")
		life_main = personal.get(u'life_main', "")
		alchohol = personal.get(u'alchohol', "")
		smoking = personal.get(u'smoking', "")
	return (deactivated, bdate, political, religion, people_main, life_main, 
		alchohol, smoking, country, city)
	
def add_user_to_db(user_info):			
	print "Adding user to database"
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
	add_relatives(user_info)

def compare_friends_with_db(user_id, friend_list):
	print "Checking friend list actuality"
	already_in_db_friends = []
	for row in cur.execute('''SELECT friend_id FROM Users_friends WHERE user_id = ( ? )''',(user_id, )):
		if row[0] not in already_in_db_friends:
			already_in_db_friends.append(row[0])
	new_friends_list = []
	deleted_friend_list = []
	for friend in friend_list: #check for new friends
		if friend not in already_in_db_friends:
			new_friends_list.append(friend)
	for friend in already_in_db_friends:
		if friend not in friend_list:
			deleted_friend_list.append(friend)	
	return new_friends_list, deleted_friend_list

def add_friends_list(user_id, friend_list):
	print "Adding user's friends to database"
	q = cur.execute('''SELECT * FROM Users_friends WHERE user_id = ( ? ) ''', (user_id, ))
	if q.fetchone() is None:
		for friend in friend_list:
			cur.execute('''INSERT OR IGNORE INTO Users_friends (user_id, friend_id,
				is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
				''', (user_id, friend, "1", current_date, "friend"))
	else:
		new_friends_list, deleted_friend_list = compare_friends_with_db(user_id, friend_list)
		if len(new_friends_list) > 0:
			for friend in new_friends_list:
				cur.execute('''INSERT OR IGNORE INTO Users_friends (user_id, friend_id,
					is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
					''', (user_id, friend, "1", current_date, "friend"))			
		if len(deleted_friend_list) > 0:
			for friend in deleted_friend_list:
				cur.execute('''UPDATE Users_friends SET is_actual = 0 WHERE user_id = ( ? ) and friend_id = ( ? )
					and is_actual = 1''', (user_id,  friend))
				cur.execute('''INSERT OR IGNORE INTO Users_friends (user_id, friend_id,
					is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
					''', (user_id, friend, "1", current_date, "unfriend"))

def add_group_list(user_id, group_list):
	print "Adding user's groups to database"
	q = cur.execute('''SELECT * FROM Groups_members WHERE user_id = ( ? ) ''', (user_id, ))
	if q.fetchone() is None:
		for group in group_list:
			cur.execute('''INSERT OR IGNORE INTO Groups_members (group_id, user_id,
				is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
				''', (group, user_id, "1", current_date, "member"))
	else:
		new_group_list, deleted_group_list = compare_groups_with_db(user_id, group_list)
		if len(new_group_list) > 0:
			for group in new_group_list:
				cur.execute('''INSERT OR IGNORE INTO Groups_members (group_id, user_id,
					is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
					''', (group, user_id,  "1", current_date, "member"))			
		if len(deleted_group_list) > 0:
			for group in deleted_group_list:
				cur.execute('''UPDATE Groups_members SET is_actual = 0 WHERE user_id = ( ? ) and group_id = ( ? )
					and is_actual = 1''', (user_id,  group))
				cur.execute(''''INSERT OR IGNORE INTO Groups_members (group_id, user_id,
					is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )
					''', (group, user_id, "1", current_date, "not member"))	
				
def compare_groups_with_db(user_id, group_list):
	print "Cheking group list actuality in database"
	already_in_db_groups = []
	for row in cur.execute('''SELECT group_id FROM Groups_members WHERE user_id = ( ? )''',(user_id, )):
		if row[0] not in already_in_db_groups:
			already_in_db_groups.append(row[0])
	new_group_list = []
	deleted_group_list = []
	for group in group_list: #check for new groups
		if group not in already_in_db_groups:
			new_group_list.append(group)
	for group in already_in_db_groups:
		if group not in group_list:
			deleted_group_list.append(group)	
	return new_group_list, deleted_group_list
	
def update_Groups_table(group_id, group_info):
	#add info about group to database
	print "Updating info about group in database"
	if check_if_group_exist(group_id) is False:
		add_group_to_db(group_info)
	else:
		if check_if_group_actual(group_id, group_info) is not True:
			cur.execute('''UPDATE Groups SET is_actual = 0 WHERE gid = ( ? ) 
				and is_actual = 1''', (group_id, ))
			add_group_to_db(group_info)
	connection.commit()

def update_Users_tables(id_list, count):
	print "Add to database list of group's members and their info"
	x = 1
	for user_id in id_list:
		print "Getting user info for %s of %s" % (x, count)
		user_info, friend_list, group_list = get_user_info(user_id)
		add_friends_list(user_id, friend_list)
		add_group_list(user_id, group_list)
		if check_if_user_exist(user_id) is False:
			add_user_to_db(user_info)
		else: 
			if check_if_user_actual(user_id, user_info) is not True:
				cur.execute('''UPDATE Users SET is_actual = 0 WHERE uid = ( ? ) 
					and is_actual = 1''', (user_id, ))
				add_user_to_db(user_info)

		x += 1
	connection.commit()			

def group_members_by_group_info(group_id, id_list): 
#even if user prefer ro hide that information, we can still see him in group's own list of members
	print "Adding to database list of group members from group info"
	for id in id_list:
		q = cur.execute('''SELECT * FROM Group_list_members WHERE user_id = ( ? ) and group_id = ( ? )''', (id, group_id))
		if q.fetchone() is None:
			cur.execute('''INSERT OR IGNORE INTO Group_list_members (user_id, group_id,
				is_actual, date_actual, status) VALUES ( ?, ?, ?, ?, ? )''', 
				(id, group_id, "1", current_date, "member"))
	connection.commit()	

def create_group_list_from_db():
	print "Create list of groups based on groups.get-method" 
	group_ids = []
	for row in cur.execute('''SELECT group_id FROM Groups_members'''):
		if row[0] not in group_ids:
			group_ids.append(row[0])
	return group_ids	

group_id = '38532412' #vk.com/privivkanet
current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())

connection = sqlite3.connect('vk_vaccination.db')
cur = connection.cursor()

print "Connected to database\n * * * \n"

token = open("token.txt").read()
vk = vkontakte.API(token=token)

group_info, count = get_group_info(group_id)
update_Groups_table(group_id, group_info)

id_list = get_user_id(group_id, count)
group_members_by_group_info(group_id, id_list)
				
update_Users_tables(id_list, count)

users_group_ids = create_group_list_from_db()
suspicios_groups = []

for id in users_group_ids:
	x = 1
	print "Getting data for group #", x, "of", len(users_group_ids)
	user_group_info, user_count = get_group_info(id)
	update_Groups_table(id, user_group_info)
	if user_count > 20000:
		suspicios_groups.append(user_group_info)
		continue
	else:
		user_id_list = get_user_id(id, user_count)
		group_members_by_group_info(id, user_id_list)
	x+=1

print suspicios_groups
	
with open("groups.txt", "w") as text_file:
    text_file.write(suspicios_groups)