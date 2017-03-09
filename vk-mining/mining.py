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

group_id = 'joinrpg' #vk.com/privivkanet
current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())

#getting info about start group
group_info, count, contacts, links = group.get_info(group_id)
members_ids = group.get_members_ids(group_id, count)

#write_to_db.update_Groups_table(group_info)

if len(contacts) > 0:
	if len(raw_input("Update contacts? ")) > 0:
		write_to_db.update_group_contacts(group_info, contacts)
			
if links is not None:
	if len(raw_input("Update links? ")) > 0:
		print "Update links?"

write_to_db.commited()