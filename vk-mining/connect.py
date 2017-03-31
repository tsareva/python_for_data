#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import group
import write_to_db
import time, sqlite3, vkontakte
from pygraphml import Graph
from pygraphml import GraphMLParser

def get_url(link):
	full_url = link[u'url']
	s = full_url.index("://")+3
	if full_url.find("vk.com") is -1:
		if full_url[s:].find("/") is not -1:
			e = full_url[s:].index("/")+s
			url = full_url[s:e]
		else:
			url = full_url[s:]
	else:
		url = full_url[s:]
	url = url.replace("www.", "")	
	return url

def create_graph(graph, group_id, links):
	print "There are %s links" % len(links)
	group_list = []
	for link in links:
		url = get_url(link)
		l = g.add_node(url)
		g.add_edge_by_label(group_id, url)
		if url.find("vk.com") is -1:
			l['type'] = "site"
		elif url.find("vk.com") is not -1:
			l['type'] = "vk"
			l['label'] = l['label'].replace("vk.com/","")
			if l['label'].find("wall") is -1:
				group_list.append(l['label'])
	return group_list

group_id = 'rosmolodez' # start group to search for connections
current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())

group_info, count, contacts, links = group.get_info(group_id)

g = Graph()

sgroup = g.add_node(group_id)
group_list = create_graph(g, group_id, links)
for id in group_list:
	group_info, count, contacts, links = group.get_info(id)
	time.sleep(0.2)
	if links is not None:
		group_list_next = create_graph(g, id, links)
		for id_next in group_list_next:
			group_info, count, contacts, links = group.get_info(id_next)
			time.sleep(0.2)
			if links is not None:
				create_graph(g, id_next, links)



graphname = group_id+"Graph.graphml"
	
parser = GraphMLParser()
parser.write(g, graphname)