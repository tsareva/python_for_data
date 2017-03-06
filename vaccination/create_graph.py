from pygraphml import Graph
from pygraphml import GraphMLParser
import sqlite3

connection = sqlite3.connect('test.db')
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
	for row in cur.execute('SELECT id1, id2 FROM Friend_list'):
		friend_connections.append(row)
	return friend_connections

g = Graph()	
node_list = []
for row in cur.execute('SELECT node_id FROM Ids'):
	node_list.append(row[0])
for node in node_list:
	g.add_node(node)
	
id_with_memb = dict()	
for node in node_list:
	members = []
	for row in cur.execute('SELECT id1 FROM Connections WHERE id2 = ( ? )', (node, )):
		members.append(row[0])
	id_with_memb[node] = members

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