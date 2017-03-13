#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3, time

connection = sqlite3.connect('vk_vaccination.db')
cur = connection.cursor()
current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())

print "Connected to database\n * * * \n"

def check_if_group_exist(group_info):
	gid = group_info[u'gid']
	q = cur.execute('''SELECT * FROM Groups WHERE gid = ( ? )''', (gid, ))
	if q.fetchone() is None:
		return False
	else:
		print "Group already in database"
		return True

def check_if_group_actual(group_info):
	gid = group_info[u'gid']
	cur.execute('''SELECT * FROM Groups 
		WHERE gid = ( ? ) AND is_actual = 1''', (gid, ))
	row = cur.fetchone()
	if (group_info[u'name'] == row[4]
			and group_info[u'screen_name'] == row[5]
			and group_info[u'type'] == row[6] 
			and group_info[u'is_closed'] == row[7]
			and group_info['description'] == row[8]):
		print "Info for group is actual"
		return True

def add_group_to_db(group_info):
	cur.execute('''
		INSERT OR IGNORE INTO Groups (gid, is_actual, date_actual, 
			name, screen_name, type, is_closed, description) 
		VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )
		''', (group_info[u'gid'], "1", current_date, group_info[u'name'],  
				group_info[u'screen_name'], group_info[u'type'], 
				group_info[u'is_closed'], group_info['description']))
	print "Add info about group %s into database" % group_info[u'gid']

def add_group_count(group_id, count):
	q = cur.execute('''SELECT * FROM Group_count 
		WHERE group_id = ( ? ) and count = ( ? )''', (group_id, count ))
	if q.fetchone() is None:
		cur.execute('''
			INSERT OR IGNORE INTO Group_count (group_id, date_actual, count) 
			VALUES ( ?, ?, ? )''', (group_id, current_date, count))	
	
def update_Groups_table(group_info):
	#add info about group to database
	print "Updating info about group in database"
	if check_if_group_exist(group_info) is False:
		add_group_to_db(group_info)
	else:
		if check_if_group_actual(group_info) is not True:
			cur.execute('''UPDATE Groups SET is_actual = 0 WHERE gid = ( ? ) 
				and is_actual = 1''', (group_info[u'gid'], ))
			add_group_to_db(group_info)
	
def add_group_contact(gid, contact):
	cur.execute('''
		INSERT OR IGNORE INTO Contacts (group_id, user_id, is_actual, 
		date_actual, desc, phone, email) 
		VALUES ( ?, ?, ?, ?, ?, ?, ? )''', 
		(gid, contact.get(u'user_id', ""), "1", current_date, 
			contact.get(u'desc', ""), contact.get(u'phone', ""), 
			contact.get(u'email', "")))

def check_if_contact_actual(gid, contact):
	cur.execute('''SELECT * FROM Contacts 
		WHERE group_id = ( ? ) AND user_id = ( ? ) 
		AND is_actual = 1''', (gid, contact.get(u'user_id', "")))
	row = cur.fetchone()
	if row is None:
		return False
	else:
		if (contact.get(u'desc', "") == row[5] and contact.get(u'phone', "") == row[6]
				and contact.get(u'email', "") == row[7]):
			return True
		else:
			cur.execute('''UPDATE Contacts SET is_actual = 0
				WHERE group_id = ( ? ) AND user_id = ( ? ) 
				AND is_actual = 1''', (gid, contact.get(u'user_id', "")))
			return False
		
def update_group_contacts(group_info, contacts):
	gid = group_info[u'gid']
	if contacts is None:
		pass
	else:
		for contact in contacts:
			if check_if_contact_actual(gid, contact) is False:
				add_group_contact(gid, contact)

def add_group_link(gid, link):
	cur.execute('''
		INSERT OR IGNORE INTO Links (group_id, lid, is_actual, 
		date_actual, url, name, desc) 
		VALUES ( ?, ?, ?, ?, ?, ?, ? )
		''', (gid, link[u'id'], "1", current_date, link[u'url'], link[u'name'], link[u'desc']))

def check_if_link_actual(gid, link):
	cur.execute('''SELECT * FROM Links 
		WHERE group_id = ( ? ) AND lid = ( ? ) 
		AND is_actual = 1''', (gid, link[u'id']))
	row = cur.fetchone()
	if row is None:
		return False
	else:
		if (link[u'url'] == row[5] and link[u'name'] == row[6] and link[u'desc'] == row[7]):
			return True
		else:
			cur.execute('''UPDATE Links SET is_actual = 0
				WHERE group_id = ( ? ) AND lid = ( ? ) 
				AND is_actual = 1''', (gid, link[u'id']))
			return False
		
def update_group_links(group_info, links):
	gid = group_info[u'gid']
	if links is None:
		pass
	else:
		for link in links:
			if check_if_link_actual(gid, link) is False:
				add_group_link(gid, link)			

def add_group_member(member):
	cur.execute('''
		INSERT OR IGNORE INTO Groups_members (group_id, user_id, is_actual, 
		date_actual, status, source) VALUES ( ?, ?, ?, ?, ?, ? )''', 
		(member[0], member[1], "1", current_date, "member", member[2]))

def compare_groups_with_db(memberships):
	for member in memberships:
		cur.execute('''SELECT group_id, user_id, source FROM Groups_members 
			WHERE group_id = ( ? ) AND user_id = ( ? ) AND source = ( ? ) AND is_actual = 1''', 
			(member[0], member[1], member[2]))
		row = cur.fetchone()
		if row is None:
			add_group_member(member)
			
def select_unique_groups_from_db():
	group_list = []
	for row in cur.execute('''SELECT DISTINCT group_id FROM Groups_members'''):
		group_list.append(row[0])
	return group_list
				
def commited():
	connection.commit()