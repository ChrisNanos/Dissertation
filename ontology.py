import networkx as nx
import matplotlib.pyplot as plt

edges = [['laptop', 'table'], ['laptop', 'bowl'], ['bowl', 'table'], ['plant', 'table'],
         ['plant', 'vase'], ['laptop', 'plant']]
G = nx.DiGraph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)
plt.figure()
nx.draw_networkx(G, pos, arrows=True, edge_colour='black', width=1, linewidths=1, node_size=500,
                 node_color='pink', alpha=0.9, labels={node: node for node in G.nodes()})
nx.draw_networkx_edge_labels(G, pos, edge_labels={('table', 'laptop'): 'on top of', ('table', 'plant'): 'on top of',
                                                  ('table', 'bowl'): 'on top of', ('laptop', 'plant'): 'right of',
                                                  ('vase', 'plant'): 'inside of', ('bowl', 'laptop'): 'left of'},
                             font_color='red')
plt.axis('off')
plt.show()

# edges = [['A', 'B'], ['B', 'C'], ['B', 'D']]
# G = nx.Graph()
# G.add_edges_from(edges)
# pos = nx.spring_layout(G)
# plt.figure()
# nx.draw(G, pos, edge_color='black', width=1, linewidths=1, node_size=500, node_color='pink', alpha=0.9,
#         labels={node: node for node in G.nodes()})
# nx.draw_networkx_edge_labels(G, pos, edge_labels={('A', 'B'): 'AB', ('B', 'C'): 'BC', ('B', 'D'): 'BD'},
#                              font_color='red')
# plt.axis('off')
# plt.show()

# G.add_edges_from([(1, 2), (1, 3)])
# G.add_node(1)
# G.add_edge(1, 2)
# G.add_node("spam")        # adds node "spam"
# G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
# G.add_edge(3, 'm')
#
# print("G.number_of_nodes()")
# print(G.number_of_nodes())
# print("G.number_of_edges()")
# print(G.number_of_edges())
# print("list(G.nodes)")
# print(list(G.nodes))
# print("G.edges")
# print(G.edges)
# print("list(G.adj[1]")  # or list(G.neighbors(1))
# print(list(G.adj[1]))
# print("G.degree[1]")  # the number of edges incident to 1
# print(G.degree[1])
# print("G.edges([2, 'm'])")
# print(G.edges([2, 'm']))
# print("G.degree([2, 3])")
# print(G.degree([2, 3]))
#
# G.remove_node(2)
# G.remove_nodes_from("spam")
# G.remove_edge(1, 3)
#
# G.add_edge(1, 2)
# H = nx.DiGraph(G)   # create a DiGraph using the connections from G
# print("list(H.edges())")
# print(list(H.edges()))
#
# edgelist = [(0, 1), (1, 2), (2, 3)]
# H = nx.Graph(edgelist)
