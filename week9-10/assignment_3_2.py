import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import numpy as np
import os
import pandas as pd
from  collections import Counter 
import time
from multiprocessing import Pool
import platform

"""
Q3.
(25 pts) 
Given a network in which nodes have different attributes, we might be interested in
predicting node labels. For example, in a social network some users might specify their gender
while others may not. We would like to use the network structure to predict the gender of nodes
without labels. One of the most straightforward approaches to addressing this problem is known
as the “guilt by association” heuristic. Here we predict the label of a node based on the most
common label of its neighbors where ties are broken randomly. This tends to work well when the
network structure is assortative with respect to the given label.
Consider the undirected version of the PubMed Diabetes network where nodes are classified as 1
(Diabetes Mellitus, Experimental), 2 (Diabetes Mellitus Type 1), or 3 (Diabetes Mellitus Type
2). For a given p between 0 and 1, pick a random fraction p of the nodes for which to observe
labels. Predict labels for the remaining nodes using the guilt by association heuristic. Repeat this
procedure 10 times for values of p ranging from 0.1 to 0.9 in increments of 0.1 and keep track of
the average fraction of correct guesses for each p. Make a figure with p on the x-axis and average
fraction of correct labels on the y-axis.
Note that the format of the network here may be a little difficult to deal with. You will likely
need to write your own parser to use the information in the files to create a graph in NetworkX.
"""



def readDiabetesdata(edgeFile, labelFile):
    G = readDiabetesLabels(labelFile)

    with open(edgeFile, 'r') as f:
        #skip the first two lines
        f.readline()
        f.readline()
        for line in f:
            line = line.strip().split() #no arg = split by space
            u = line[1].split(":")[1]
            v = line[-1].split(":")[1]
            if u ==v: #avoid self loop
                continue
            nodes=[]
            for i in G.edges(u):
                nodes.append(i[1])
            #erase self loop and duplicatd edges
            if v not in nodes:
                G.add_edge(u,v)
            
    return G

def readDiabetesLabels(labelFile):
    G = nx.Graph()

    with open(labelFile, 'r') as f:
        f.readline()
        f.readline()
        for line in f:
            line = line.strip().split()
            u = line[0]
            label = line[1].split("=")[1]
            # print(label)
            G.add_node(u,label=label)

    return G
    

if __name__ == "__main__":
    edgeFile = "./pubmed-diabetes/data/Pubmed-Diabetes.DIRECTED.cites.tab"
    labelFile = "./pubmed-diabetes/data/Pubmed-Diabetes.NODE.paper.tab"
    G = readDiabetesdata(edgeFile=edgeFile, labelFile=labelFile)

    for p in np.arange(0.1,1.0,0.1):
        for _ in range(10):
            label_nodes = {}
            nodes = np.random.choice(G.nodes(), size=int(p*len(G)), replace=False)
            print(len(nodes))
            #initialize the label of all the nodes except the randomly chosen nodes
            for v in G.nodes():
                if v in nodes:
                    continue
                else:
                    label_nodes[v] =int(G.nodes[v]["label"]) #store the previous label so that we can compare if the predicted label is the same the actual one
                    G.nodes[v]["label"] = "0"
            success_counter=0
            total_counter=0
            for v in G.nodes():
                if v in nodes: #if the node is in the chosen nodes 
                    continue
                else:
                    total_counter+=1
                    labels = [0,0,0]
                    print(v, "neighbors:")
                    for u in G.neighbors(v): #check all the neighbors of v to use guild by association heuristic
                        _label = nx.get_node_attributes(G, "label")[u]
                        if int(_label) == 1:
                            labels[0] +=1
                        elif int(_label) == 2:
                            labels[1] +=1
                        elif int(_label) == 3:
                            labels[2] +=1
                    _max =[]
                    index = labels.index(max(labels))
                    _max.append(index+1)
                    for i in range(len(labels)):
                        if index == i:
                            continue
                        elif labels[i] == labels[index]:
                            _max.append(i+1)
                    prob = 1.0/len(_max)
                    prob_list = [prob] * len(_max)
                    node_label = np.random.choice(_max, p =prob_list)
                    if node_label == label_nodes[v]:
                        # print("same!")
                        success_counter+=1
                    else:
                        # print("different...")
                        pass
            print(p, "prob:", float(success_counter/total_counter))
# def _mean_estimate(G):
#     for p in np.arange(0.1,1.0,0.1):
#         estimates ={}
#         for _ in range(100):
#             nodes = np.random.choice(G.nodes(), size=int(p*len(G)), replace=False)
#             estimates[p] = estimates.get(p,[]) + [np.mean([G.degree(v) for v in nodes])]
#         print("Mean estimate", p,np.mean(estimates[p]))  
#     return nodes


# if __name__ == "__main__":
#     G = nx.read_edgelist("./H-I-05.tsv")
#     E = list(G.edges())

#     Gp = G.subgraph(max(nx.connected_components(G)))
#     #tuue values
#     print("AVEERAGE DEGREE", np.mean([Gp.degree(i) for i in Gp.nodes()]))

#     nodes = _mean_estimate(G)


#     print("induced subgraph")
#     Ginducded =G.subgraph(nodes)
#     # nodes = _mean_estimate(Ginducded)
#     ps = []
#     induced_esimate_means =[]
#     for p in np.arange(0.1,1.0,0.1):
#         estimates ={}
#         for _ in range(100):
#             nodes = np.random.choice(G.nodes(), size=int(p*len(G)), replace=False)
#             H = G.subgraph(nodes)
#             estimates[p] = estimates.get(p,[]) + [np.mean([H.degree(v) for v in nodes])]
#         ps.append(p)
#         induced_esimate_means.append(np.mean(estimates[p]))
#         print("Mean estimate", p,np.mean(estimates[p]))  

#     print("incident subgraph")
#     Gincident = G.edge_subgraph(G.edges())
#     incident_estimate_means =[]
#     for p in np.arange(0.1,1.0,0.1):
#         estimates ={}
#         for _ in range(100):
#             edges = np.random.choice(len(E), size=int(p*len(E)), replace=False)
#             edges = ([E[e] for e in edges])
#             H = G.edge_subgraph(edges)
#             estimates[p] = estimates.get(p,[]) + [np.mean([H.degree(v) for v in H.nodes()])]
#         incident_estimate_means.append(np.mean(estimates[p]))
#         print("Mean estimate", p,np.mean(estimates[p]))  

#     for i in range(len(incident_estimate_means)):
#         incident_estimate_means[i] = incident_estimate_means[i]/len(incident_estimate_means)
#         induced_esimate_means[i] = induced_esimate_means[i]/len(induced_esimate_means)

#     plt.figure()    
#     # plt.subplot(221)
#     plt.scatter(ps, induced_esimate_means, color="red",label='Induced subgraph',alpha=0.3, edgecolors='none')
#     plt.scatter(ps, incident_estimate_means, color="green",label='Incident subgraph',alpha=0.3, edgecolors='none')
#     # plt.yscale("log")
#     plt.xlabel('probabilities')
#     plt.ylabel('average fraction of correct guesses')
#     plt.title('Guilt by association heuristic')
#     plt.legend()
#     plt.show()

#     print("AVEERAGE DEGREE", np.mean([Gp.degree(i) for i in Gp.nodes()]))



#     print("DEGREEE DISTRIBUTION")

    

    print("DIAMETER", nx.diameter(Gp))

    print("GLOBAL CLUSTERING COEFFICIENT", nx.transitivity(Gp))

    """
    I just collected all the estimate mean for each probability for both induced and incident graphs.
    And I made a plot with those information
    But is there anything I need to do more?
    """

