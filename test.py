import networkx as nx
import matplotlib.pyplot as plt








B = nx.Graph()
B.add_nodes_from([1, 2, 3, 4], bipartite=0)
B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
Y = set(B) - X

X = sorted(X, reverse=True)
Y = sorted(Y, reverse=True)

pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
nx.draw(B, pos=pos, with_labels=True)
plt.show()