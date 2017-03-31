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

group_info, count, contacts, links = group.get_info(group_id)
group_id = group_info[u'gid']

posts = messages.get_wall_messages(group_id)
for post in posts[:10]:
	post_dict = messages.get_message_info(posts)
	write_to_db.update_message(post_dict)
write_to_db.commited()