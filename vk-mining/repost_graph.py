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

source = raw_input("Enter id for start group: ")
m_id = raw_input("Enter id for start message: ")
filename = source + "-message" + m_id + '-reposts.csv'
group_id = source + "-message" + m_id

data, fieldnames = work_with_csv.read_csv_file(filename)

node = g.add_node(source) #start message
node['membership'] = "start post"

for row in data:
	node = g.add_node(row[4])
	node['unixdate'] = row[1]
	node['source'] = row[5]
	node['copy_text'] = row[8]
	node['reposter type'] = row[9]
	if int(row[4]) < 0:
		node['membership'] = "group"
	elif row[4] in list:
		node['membership'] = "group's member"

for row in data:
	n1 = row[4]
	n2 = row[5]
	g.add_edge_by_label(n1, n2)
	
graphname = group_id+"Graph.graphml"
	
parser = GraphMLParser()
parser.write(g, graphname)