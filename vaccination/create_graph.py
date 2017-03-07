from pygraphml import Graph
from pygraphml import GraphMLParser
import sqlite3

connection = sqlite3.connect('vk_vaccination.db')
cur = connection.cursor()

def create_friend_graph(friend_connections):
	g = Graph()
	for edge in friend_connections:
		n1 = str(edge[0])
		n2 = str(edge[1])
		g.add_edge_by_label(n1, n2)
	return g

def create_friend_connections():
	friend_connections = []
	for row in cur.execute('SELECT user_id, friend_id FROM User_friends'):
		friend_connections.append(row)
	return friend_connections

g = Graph()	
node_list = []
for row in cur.execute('SELECT DISTINCT group_id FROM Groups_members WHERE id <1001'):
	if row[0] not in node_list:
		node_list.append(row[0])
		print "Add node with id", row[0]
print "Created list of %s nodes" % len(node_list)

for node in node_list:
	g.add_node(node)
print "Added nodes to graph"

n = 1	
id_with_memb = dict()	
for node in node_list:
	print "Work with node %s of %s" % (x, len(node_list))
	members = []
	for row in cur.execute('SELECT user_id FROM Groups_members WHERE group_id = ( ? )', (node, )):
		members.append(row[0])
	id_with_memb[node] = members
	n+=1
print "Finish upload group members"

x = 0	
for node in node_list:
	print "Work with node %s of %s" % (x, len(node_list))
	users = id_with_memb[node]
	del id_with_memb[node]
	for id, memb in id_with_memb.iteritems():
		for user in users:
			if user in memb:
				n1 = str(node)
				n2 = str(id)
				g.add_edge_by_label(n1, n2)
	x+=1
	
parser = GraphMLParser()
parser.write(g, "myGraph.graphml")