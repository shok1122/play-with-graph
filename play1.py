import random
import requests
import sys
import networkx as nx
import pprint

from py2cytoscape.data.cyrest_client import CyRestClient

args = sys.argv[1:]

seed = args[0]

random.seed(seed)

graph_size = 20
graph_size_range = graph_size / 2

edge_num_limit = 3
hub_node_prob = 0.1

num_v = random.randrange(graph_size - graph_size_range, graph_size + graph_size_range)

g = nx.MultiDiGraph()

for i in range(num_v):
    i_hub = False
    o_hub = False
    if random.random() < hub_node_prob:
        i_hub = True
    if random.random() < hub_node_prob:
        o_hub = True
    g.add_node(i, i_hub=i_hub, o_hub=o_hub)

for x in range(num_v):
    tmp = []
    e_min = 0
    e_max = edge_num_limit
    if g.node[x]['o_hub']:
        e_min = edge_num_limit * 2
        e_max = edge_num_limit * 3
    for i in range(random.randrange(e_min, e_max)):
        y = random.randrange(0, num_v)
        if x != y and y not in tmp:
            tmp.append(y)
            g.add_edge(x,y)

for y in g.nodes_iter():
    if not g.node[y]['i_hub']:
        continue
    for i in range(edge_num_limit):
        x = random.randrange(0, num_v)
        if y in g.edge[x]:
            continue
        if x == y:
            continue
        g.add_edge(x,y)

print('Number of Nodes: ' + str(g.number_of_nodes()))
print('Number of Edges: ' + str(g.number_of_edges()))

cy = CyRestClient()
nw = cy.network.create(name='My Network', collection='My network collection')

g_cy = cy.network.create_from_networkx(g)

layout = cy.style.create('Directed')
cy.layout.apply(name='kamada-kawai', network=g_cy)
cy.style.apply(layout, network=g_cy)
cy.edgebundling.apply(g_cy)

