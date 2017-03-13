#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import group
import write_to_db
import time, sqlite3, vkontakte
import pprint

group_id = '140159421' #vk.com/privivkanet
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

#all_groups_from_users = group.create_all_groups_from_users(members_ids)
#write_to_db.compare_groups_with_db(all_groups_from_users)
#write_to_db.commited()

groups_from_db = write_to_db.select_unique_groups_from_db()
str_group_ids = ','.join(str(e) for e in groups_from_db)
many_group_info = group.get_info_for_many_groups(str_group_ids)
len(many_group_info)
	
#if len(contacts) > 0:
#	if len(raw_input("Update contacts? ")) > 0:
#		None
			
#if links is not None:
#	if len(raw_input("Update links? ")) > 0:
#		None

