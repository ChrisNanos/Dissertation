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
