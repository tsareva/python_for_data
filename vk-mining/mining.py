#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import group
import write_to_db
import messages
import time, sqlite3, vkontakte
import pprint

group_id = 'privivkanet' #vk.com/privivkanet
current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())

#getting info about start group
group_info, count, contacts, links = group.get_info(group_id)
group_id = group_info[u'gid']
members_ids = group.get_members_ids(group_id, count)
memberships = group.create_memberships(members_ids, group_id, "group info")
write_to_db.compare_groups_with_db(memberships)
write_to_db.add_group_count(group_id, count)
write_to_db.update_Groups_table(group_info)
write_to_db.update_group_contacts(group_info, contacts)
write_to_db.update_group_links(group_info, links)
write_to_db.commited()

#getting info about groups in which members of start group are
if len(raw_input("Get info about groups in which members of start group are?")) > 0:
	all_groups_from_users = group.create_all_groups_from_users(members_ids)
	write_to_db.compare_groups_with_db(all_groups_from_users)
	write_to_db.commited()

groups_from_db = write_to_db.select_unique_groups_from_db()
print "There are %s groups in database" % len(groups_from_db)

s = 0
e = 10000
if len(groups_from_db) > 1:
	if len(raw_input("Get profiles for all groups?")) > 0:
		l = 0
		while (e-10000) < len(groups_from_db):
			many_group_info = group.get_info_for_many_groups(groups_from_db[s:e])
			for all_group_info in many_group_info:
				group_info, count, contacts, links = group.reshape_info_from_many_groups(all_group_info)
				group_id_from_db = group_info[u'gid']
				write_to_db.add_group_count(group_id_from_db, count)
				write_to_db.update_Groups_table(group_info)
				write_to_db.update_group_contacts(group_info, contacts)
				write_to_db.update_group_links(group_info, links)
			s+=10000
			e+=10000
			l+=10000
			print "%s of %s done" % (l, len(groups_from_db))
			write_to_db.commited()

posts = messages.get_wall_messages(group_id)
for post in posts[:10]:
	post_dict = messages.get_message_info(posts)
	write_to_db.update_message(post_dict)
write_to_db.commited()
	


#messages_list = write_to_db.select_messages_id()
#g_id = group_id * (-1)
#comments = messages.get_comments(g_id, messages_list[1])
#print type(comments[1])