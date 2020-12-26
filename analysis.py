import twint  # library crawl sthe teitter and fetches back data no need of API tokens
import pandas as pd  # to make the data extraction easier
import networkx as nx  # Main library used to create a graph and run the network measures
import matplotlib.pyplot as plt  # for drawing the created graphs
import collections  # for extracting data from the dicts easily
import json

graph = nx.DiGraph()  # init a directed graph
users = 'imVkohli'  # randomly choosed a user # chuchu_DK
limit = 10  # limited the followers list so that processing will be quicker


def get_followings(username):
    c = twint.Config()  # config object init
    c.Username = username
    c.Pandas = True
    c.Limit = limit
    twint.run.Following(c)
    list_of_followings = twint.storage.panda.Follow_df
    return list_of_followings['following'][username]


def get_followers(username):
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    c.Limit = limit
    twint.run.Followers(c)
    list_of_followers = twint.storage.panda.Follow_df
    return list_of_followers['followers'][username]


def save(G, fname):
    json.dump(dict(nodes=[[n, G.nodes[n]] for n in G.nodes()],
                   edges=[[u, v] for u, v in G.edges()]),
              open(fname, 'w'), indent=2)


def load(fname):
    G = nx.DiGraph()
    d = json.load(open(fname))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
    return G


print("Do you want to Fetch fresh data(YES) or use prefetched data(NO)?")
#phase 1
if(input() == "YES"):
    # followers = get_followers(users)
    # print("Adding followers relationships...")
    # for user in followers:
    #     graph.add_edge(user, users)

    following = get_followings(users)
    json.dump(following,open('input/'+users+'-data.json', 'w'), indent=2)
    print("Adding following relationships...")
    for user in following:
        graph.add_edge(users, user)

    for friend in graph.nodes:
        f = get_followings(friend)
        json.dump(following,open('input/'+friend+'-data.json', 'w'), indent=2)
        for user in f:
            graph.add_edge(friend, user)
    save(graph,"input/data.json")
else:
    graph = load("input/data.json")
    

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
