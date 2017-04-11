#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
from pygraphml import Graph
from pygraphml import GraphMLParser
import work_with_csv
import codecs

g = Graph()

with codecs.open("19732513-profile-members.txt", 'r', 'utf-8-sig') as file:
	opened_file = file.read().split("\n")
	fieldnames = opened_file[0].split("\t")
	data_members = []
	for row in opened_file[1:]:
		data_members.append(row.split("\t"))

list = []
for row in data_members:
	list.append(row[0])

data, fieldnames = work_with_csv.read_csv_file(filename)

source = raw_input("Enter id for start group")
m_id = raw_input("Enter id for start message")
filename = source + "message" + m_id + '-reposts.csv'
group_id = source + "message" + m_id


g.add_node(source) #start message

for row in data:
	node = g.add_node(row[3])
	node['unixdate'] = row[0]
	node['source'] = row[4]
	node['copy_text'] = row[7]
	node['reposter type'] = row[8]
	if row[3] in list:
		node['membership'] = "group's member"

for row in data:
	n1 = row[3]
	n2 = row[4]
	g.add_edge_by_label(n1, n2)
	
graphname = group_id+"Graph.graphml"
	
parser = GraphMLParser()
parser.write(g, graphname)