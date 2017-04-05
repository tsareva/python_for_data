#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import work_with_csv
import group

data, fieldnames = work_with_csv.read_csv_file('ki_games.csv')
group_names = []
for row in data:
	if row[20] not in group_names:
		group_names.append(row[19])
print len(group_names)		
for group_name in group_names:
	if group_name.find('NULL') is -1:
		group_info, count, contacts, links = group.get_info(group_name)
		print group_info