import twint  # library crawl sthe teitter and fetches back data no need of API tokens
import pandas as pd  # to make the data extraction easier
import networkx as nx  # Main library used to create a graph and run the network measures
import matplotlib.pyplot as plt  # for drawing the created graphs
import collections  # for extracting data from the dicts easily
import json

graph = nx.DiGraph()  # init a directed graph
d = json.load(open('imVkohli-data.json'))
for user in d:
    graph.add_edge("imVkohli", user)
    s = json.load(open(user+'-data.json'))
    for fs in s:
        graph.add_edge(user, fs)

json.dump(dict(nodes=[[n, graph.nodes[n]] for n in graph.nodes()],
                   edges=[[u, v] for u, v in graph.edges()]),
              open("data.json", 'w'), indent=2)