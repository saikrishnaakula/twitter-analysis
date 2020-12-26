import twint  # library crawl sthe teitter and fetches back data no need of API tokens
import pandas as pd  # to make the data extraction easier
import networkx as nx  # Main library used to create a graph and run the network measures
import matplotlib.pyplot as plt  # for drawing the created graphs
import collections  # for extracting data from the dicts easily
import json

username = 'imVkohli'

limit = 10

def get_followers(username):
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    c.Limit = limit
    twint.run.Followers(c)
    list_of_followers = twint.storage.panda.Follow_df
    json.dump(list_of_followers['followers'][username], open('input/'+
        username+'-data.json', 'w'), indent=2)


get_followers(username)
d = json.load(open('input/'+username+'-data.json'))
for friend in d:
    get_followers(friend)
