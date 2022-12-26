import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import networkx.generators.small
import numpy as np

#*********************************************
#Remove pendant and isolated nodes...
def trim_degrees(graph,min_degree=2):
    g=graph.copy()
    dc=nx.degree(g)
    for n in graph.nodes():
        if dc[n]<min_degree:
            g.remove_node(n)
    return g

#*********************************************
#print network-level metrics as DataFrame...
def describe_network(graph_list,graph_names=None):
    d = pd.DataFrame()
    for i,g in enumerate(graph_list):
        if graph_names == None:
        	graph_name = g.name
        else:
            graph_name = graph_names[i]

        num_edges = g.number_of_edges()
        num_nodes = g.number_of_nodes()
        avg_degree = round(np.mean(list(dict(g.degree).values())),2)
        #median_degree
        density = nx.density(g)
        reciprocity = nx.overall_reciprocity(g)
        diameter = nx.diameter(nx.Graph(g))
        radius  = nx.radius(nx.Graph(g))
        avg_geo_distance = nx.average_shortest_path_length(g,weight='weight')
        #median_geo_distance

        d_temp = pd.DataFrame({
                        '#edges':[num_edges],
                        '#nodes':[num_nodes],
                        'avg_degree':[avg_degree],
                        'density':[density],
                        'reciprocity':[reciprocity]
                        'diameter':[diameter],
                        'radius':[radius],
                        'avg_geo_distance':[avg_geo_distance],
                        },
                    index=[graph_name])
        d = pd.concat([d,d_temp])
    return d

#*********************************************
def reach(graph_list,graph_names=None):
    d = pd.DataFrame()
    for i,g in enumerate(graph_list):
        if graph_names == None:
            graph_name = g.name
        else:
            graph_name = graph_names[i]

        try:
            clustering_coef = nx.average_clustering(g)
        except Exception as e:
            clustering_coef = e
        try:
            transitivity = nx.transitivity(g)
        except Exception as e:
            transitivity = e

        d_temp = pd.DataFrame({                               
                                'clustering_coef':[clustering_coef],
                                'transitivity':[transitivity],
                                },
                            index=[graph_name])
        d = pd.concat([d,d_temp])
    return d

#*********************************************
def centrality(graph,graph_name=None):
    g = graph
    if graph_name == None:
        graph_name = g.name
    dc = dict(nx.degree(g))
    bc = nx.betweenness_centrality(g)
    cc = nx.closeness_centrality(g)
    try:
        ec = nx.eigenvector_centrality(g)
    except Exception as e:
        s = f"{type(e).__name__}: {e}"
        ec = {}
        [ec.update({n:s}) for n in g.nodes()]
    pr = nx.pagerank(g)
    try:
        lcc = nx.clustering(g)
    except Exception as e:
        s = f"{type(e).__name__}: {e}"
        lcc = {}
        [lcc.update({n:s}) for n in g.nodes()]

    temp_df = pd.DataFrame({
        'graph':graph_name,
        'node':dc.keys(),
        'degree':dc.values(),
        'betweenness': bc.values(),
        'closeness':cc.values(),
        'eigenvector':ec.values(),
        'PageRank':pr.values(),
        'lcc':lcc.values()
        })
    return temp_df
