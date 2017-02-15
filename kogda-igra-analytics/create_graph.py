from pygraphml import Graph
from pygraphml import GraphMLParser

# Create graph

g = Graph()

n1 = g.add_node("A")
n2 = g.add_node("B")
n3 = g.add_node("C")
n4 = g.add_node("D")
n5 = g.add_node("E")

# Add attribute
n1['color'] = 'red'

g.add_edge(n1, n3)
g.add_edge(n2, n3)
g.add_edge(n3, n4)
g.add_edge(n3, n5)

parser = GraphMLParser()
parser.write(g, "myGraph.graphml")