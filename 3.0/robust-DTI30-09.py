#!/usr/bin/env python
# coding: utf-8

# In[2]:


import networkx as nx 
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
import collections
import powerlaw
import operator
import scipy.stats
import random
import math
import csv
import io
from tqdm import tqdm
import pandas as pd
from networkx.algorithms import bipartite
def random_edge(graph, del_orig=True):
    '''
    Create a new random edge and delete one of its current edge if del_orig is True.
    :param graph: networkx graph
    :param del_orig: bool
    :return: networkx graph
    '''
    edges = list(graph.edges)
    nonedges_tot = list(nx.non_edges(graph))
    nonedges = []
    for i in range(0,len(nonedges_tot)):
        if ((nonedges_tot[i][0][0] == 'D') and (nonedges_tot[i][1][0] == 'B')) or ((nonedges_tot[i][0][0] == 'B') and (nonedges_tot[i][1][0] == 'D')):
            nonedges.append(nonedges_tot[i])
    # random edge choice
    chosen_edge = random.choice(edges)
    #chosen_nonedge = random.choice([x for x in nonedges if chosen_edge[0] == x[0]])
    chosen_nonedge = random.choice([x for x in nonedges])
    print(chosen_nonedge)
    #if del_orig:
        # delete chosen edge
        #graph.remove_edge(chosen_edge[0], chosen_edge[1])
    # add new edge
    graph.add_edge(chosen_nonedge[0], chosen_nonedge[1])
    return graph

with open("dti-3.0-interactions.csv", 'r') as f:
    reader = csv.reader(f)
    my_list = list(reader)
interactions_raw = []
for iter in range(len(my_list)):
    if my_list[iter][1] != '':
        listinter = my_list[iter][1].split (";")
        for it in range (len(listinter)):
            interactiunea = [my_list[iter][0], listinter[it]]
            interactions_raw.append(interactiunea)
interactions_bi = []
my_drugs = []
my_targets = []
for i in range (0, len(interactions_raw)):
    interactions_bi.append(tuple(interactions_raw[i]))
    my_drugs.append(interactions_raw[i][0])
    my_targets.append(interactions_raw[i][1])
BG = nx.Graph()
BG.add_nodes_from(my_drugs, bipartite=0)
BG.add_nodes_from(my_targets, bipartite=1)
BG.add_edges_from(interactions_bi)

nodes = len(list(BG.nodes()))
modify_rate = 0.09
kendall_tau = []
alpha_distrib = []
xmin_distrib = []
for i in range(1, 101):
    G = BG 
    G_t = G.copy()
    ba_c = dict(G.degree(weight='weight'))
    sorted_ba_c = sorted(ba_c.items(), key=operator.itemgetter(1))
    ascending_degree_list = []
    for a,b in sorted_ba_c:
        ascending_degree_list.append(a)
    ba_c2 = dict(collections.Counter(ba_c.values()))
    results = powerlaw.Fit(np.array(list(ba_c2.values())).astype(float))
    print("Experimentul", i)
    e_o = results.power_law.alpha.copy()
    x_o = results.power_law.xmin.copy()
    for x in range(1, math.ceil(nodes*modify_rate)+1):
        nG = random_edge(G_t, del_orig=True)
        G_t = nG
    ba_c_n = dict(nG.degree(weight='weight'))
    sorted_ba_c_n = sorted(ba_c_n.items(), key=operator.itemgetter(1))
    ascending_degree_n_list = []
    for a2,b2 in sorted_ba_c_n:
        ascending_degree_n_list.append(a2)
    corr, pvalue = scipy.stats.kendalltau(ascending_degree_list, ascending_degree_n_list)
    print(corr)
    print(pvalue)
    ba_c_n2 = dict(collections.Counter(ba_c_n.values()))
    results_mod = powerlaw.Fit(np.array(list(ba_c_n2.values())).astype(float))
    print(results_mod.power_law.alpha)
    print(results_mod.power_law.xmin)
    kendall_tau.append(corr)
    alpha_distrib.append(results_mod.power_law.alpha)
    xmin_distrib.append(results_mod.power_law.xmin)
print("Average Tau: ", sum(kendall_tau)/len(kendall_tau))
print("Max Tau: ", max(kendall_tau))
print("Min Tau: ", min(kendall_tau))
print("Alpha average: ", sum(alpha_distrib)/len(alpha_distrib))
print("Max alpha: ", max(alpha_distrib))
print("Min alpha: ", min(alpha_distrib))
print("Reference alpha: ", e_o)
print("Xmin average: ", sum(xmin_distrib)/len(xmin_distrib))
print("Max xmin: ", max(xmin_distrib))
print("Min xmin: ", min(xmin_distrib))
print("Reference xmin: ", x_o)
with open("results_robust3.0.csv", mode='w', newline='') as csv_file:
    results_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    results_writer.writerow([sum(kendall_tau)/len(kendall_tau), max(kendall_tau), min(kendall_tau), sum(alpha_distrib)/len(alpha_distrib), max(alpha_distrib), min(alpha_distrib), e_o, sum(xmin_distrib)/len(xmin_distrib), max(xmin_distrib), min(xmin_distrib), x_o])


# In[ ]:




