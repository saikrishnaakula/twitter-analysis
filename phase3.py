import networkx as nx
import os
import json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import collections
import pandas as pd
from networkx.readwrite import json_graph

# users = [
#     'shakira',
#     'narendramodi',
#     'rihanna',
#     'jtimberlake',
#     'KingJames',
#     'neymarjr',
# ]
# userName = 'narendramodi'


os.system('cls' if os.name == 'nt' else 'clear')

graph = nx.DiGraph()
userName = 'namo'


def save(graph, fname):
    json.dump(dict(nodes=[[n, graph.nodes[n]] for n in graph.nodes()],
                   edges=[[u, v] for u, v in graph.edges()]),
              open(fname, 'w'), indent=2)


def load(fname):
    G = nx.DiGraph()
    d = json.load(open(fname))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
    return G


# with open('namo_followers.json') as f:
#     data = json.load(f)
# df = pd.DataFrame.from_dict(data, orient='columns')

# for ind in df.index:
#     graph.add_edge(df['username'][ind], userName)

# with open('namo_following.json') as f:
#     dataF = json.load(f)
# df1 = pd.DataFrame.from_dict(dataF, orient='columns')

# for ind in df1.index:
#     graph.add_edge(userName,df1['username'][ind] )
# # print(graph.adj)
# # print(graph.edges["namo"]["janasena_Voter"])
# save(graph, "test.json")

graph = load("data.json")

# graph is difficult to view as png so added as well this format
# nx.write_gexf(graph, "social-network.gexf")
nx.draw(graph, pos=nx.spring_layout(graph), node_size=35, alpha=0.45,
        width=0.1, edge_color='k', font_size=6, with_labels=True)
# saving the network graph for future reference
plt.savefig("output/social-network.png", dpi=600)
# plt.show()

# degree distribution measure, using in degree
degree_sequence = sorted([d for n, d in graph.in_degree()], reverse=True)
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())
fig, ax = plt.subplots()
plt.bar(deg, cnt)
plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
ax.set_xticks(deg)
ax.set_xticklabels(deg)
plt.savefig("output/degree-histogram.png", dpi=600)
# plt.show()


# calculate clustering coefficient
coeff = nx.clustering(graph)
json.dump(coeff, open("output/clustering-coeff.json", 'w'), indent=2)
# print("{:<25} {:<10}".format('NODE', 'CLUSTERING COEFFICIENT'))
# for key, value in coeff.items():
#     print("{:<25} {:<10}".format(key, value))

# calculating page rank
pr = nx.pagerank(graph)
json.dump(pr, open("output/page-rank.json", 'w'), indent=2)
# print("{:<25} {:<10}".format('NODE', 'PAGE RANK'))
# for key, value in pr.items():
#     print("{:<25} {:<10}".format(key, value))

# calculating closenesss
cc = nx.closeness_centrality(graph)
json.dump(cc, open("output/closeness.json", 'w'), indent=2)
# print("{:<25} {:<10}".format('NODE', 'CLOSENESS'))
# for key, value in cc.items():
#     print("{:<25} {:<10}".format(key, value))

# calculating betweenness
bc = nx.betweenness_centrality(graph)
json.dump(bc, open("output/betweennenss.json", 'w'), indent=2)
# print("{:<25} {:<10}".format('NODE', 'BETWEENNESS'))
# for key, value in bc.items():
#     print("{:<25} {:<10}".format(key, value))
