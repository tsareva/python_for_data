#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys, socket, ssl
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time
from create_token import create_token


token = open("files/token.txt").read()
vk = vkontakte.API(token=token)

def get_info(group_id):
	x = 1
	while True:
		try:
			print "Getting data for group ", group_id
			fields='members_count,description,contacts,links'
			all_group_info = vk.groups.getById(group_ids=group_id, fields=fields)
			all_group_info = all_group_info[0]
			group_info = create_group_info_dict(all_group_info)
			count = all_group_info.get(u'members_count', None)
			contacts = all_group_info.get(u'contacts', None)
			links = all_group_info.get(u'links', None)
			return group_info, count, contacts, links
		except (socket.gaierror, socket.timeout, ssl.SSLError):
			print "Can't create connection for %s time. Trying again..." % x
			time.sleep(1)
			x+=1
			continue
		except vkontakte.api.VKError as error:
			if error.code == 5:
				create_token()
			continue
			
def get_info_for_many_groups(groups_from_db):
	x = 1
	s = 0
	e = 150
	many_group_info = []
	print "Getting data for %s groups" % len(groups_from_db)
	fields='members_count,description,contacts,links'
	while (len(groups_from_db) > len(many_group_info)):
		try:
			group_ids = ','.join(str(e) for e in groups_from_db[s:e])
			new_info = vk.groups.getById(group_ids=group_ids, fields=fields)
			many_group_info+=new_info
			print "Getting info for %s of %s groups" % (len(many_group_info), len(groups_from_db))
			s += 150
			e += 150
			time.sleep(0.2)
		except (socket.gaierror, socket.timeout, ssl.SSLError):
			print "Can't create connection for %s time. Trying again..." % x
			time.sleep(1)
			x+=1
			continue
	return many_group_info			
			
def reshape_info_from_many_groups(all_group_info):
	group_info = create_group_info_dict(all_group_info)
	count = all_group_info.get(u'members_count', None)
	contacts = all_group_info.get(u'contacts', None)
	links = all_group_info.get(u'links', None)
	return group_info, count, contacts, links
			
def create_group_info_dict(all_group_info):
	group_info = dict()
	group_info[u'gid'] = all_group_info.get(u'gid', "")	
	group_info[u'name'] = all_group_info.get(u'name', "")
	group_info[u'screen_name'] = all_group_info.get(u'screen_name', "")	
	group_info[u'type'] = all_group_info.get(u'type', "")	
	group_info[u'is_closed'] = all_group_info.get(u'is_closed', "")		
	group_info[u'description'] = all_group_info.get(u'description', "")
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
	
def create_memberships(members_ids, group_id, source):
	memberships = []
	for id in members_ids:
		member = (group_id, id, source)
		memberships.append(member)
	return memberships

def get_groups_for_users(user_id):
	try:
		group_list = vk.groups.get(user_id=user_id)
		time.sleep(0.2)
		return group_list
	except:
		group_list = []
		return group_list

def create_all_groups_from_users(members_ids):		
	all_groups_from_users = []
	u = 1
	for user_id in members_ids:
		print "Getting info about groups for %s of %s" % (u, len(members_ids))
		group_list = get_groups_for_users(user_id)
		user = [user_id]
		for group_id in group_list:
			groups = create_memberships(user, group_id, "user info")
			all_groups_from_users += groups
		u+=1
	return all_groups_from_users
	
