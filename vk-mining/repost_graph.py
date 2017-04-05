#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
from pygraphml import Graph
from pygraphml import GraphMLParser
import work_with_csv

g = Graph()

filename = '-18901857-message778365-reposts.csv'
group_id = '-18901857-message778365'

data, fieldnames = work_with_csv.read_csv_file(filename)

g.add_node('-18901857') #start message

for row in data:
	node = g.add_node(row[3])
	node['unixdate'] = row[0]
	node['source'] = row[4]
	node['copy_text'] = row[7]
	node['reposter type'] = row[8]

for row in data:
	n1 = row[3]
	n2 = row[4]
	g.add_edge_by_label(n1, n2)
	
graphname = group_id+"Graph.graphml"
	
parser = GraphMLParser()
parser.write(g, graphname)