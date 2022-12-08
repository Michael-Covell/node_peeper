import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import networkx.generators.small
import numpy as np

files = {'kite' : nx.generators.small.krackhardt_kite_graph(),
         'ACME_advice' : nx.read_pajek(r"C:\Users\mcove\OneDrive\mcard\ACME_advice.net.txt"),
         'orgchart' : nx.read_pajek(r"C:\Users\mcove\OneDrive\mcard\ACME_orgchart.net.txt"),
         'econom' : nx.read_pajek(r"C:\Users\mcove\OneDrive\mcard\economic.net.txt"),
         #'retweets' : nx.read_pajek(r"C:\Users\mcove\OneDrive\mcard\egypt_retweets.net.txt"),
         'military' : nx.read_pajek(r"C:\Users\mcove\OneDrive\mcard\military.net.txt"),
         #'russians' : nx.read_pajek(r"C:\Users\mcove\OneDrive\mcard\russians.net.txt")}
         'sml_wrld' : nx.navigable_small_world_graph(4),
         'rand' : nx.fast_gnp_random_graph(10,.5),
         'scale_free_graph' : nx.scale_free_graph(10),
         'cycle_graph' : nx.cycle_graph(10),
         'regular': nx.random_regular_graph(3,10)
         }

def centrality(graph_list):
    df = pd.DataFrame()
    for g in graph_list:
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
            'graph':g.name,
            'node':dc.keys(),
            'degree':dc.values(),
            'betweenness': bc.values(),
            'closeness':cc.values(),
            'eigenvector':ec.values(),
            'PageRank':pr.values(),
            'lcc':lcc.values()
            })
        df = pd.concat([df,temp_df])
    return df

#Remove pendant and isolated nodes...
def trim_degrees(g,min_degree=2):
    g2=g.copy()
    dc=nx.degree(g2)
    for n in g.nodes():
        if dc[n]<min_degree:
            g2.remove_node(n)
    return g2

#print variables
variables = ['variables:','files','centrality'] + list(files.keys())
print('\n\t-'.join(variables))

#print network-level metrics as DataFrame...
d = pd.DataFrame()
for variable_name,g in files.items():
    g = trim_degrees(g,min_degree=1)

    num_edges = g.number_of_edges()
    num_nodes = g.number_of_nodes()
    density = round(nx.density(g),2)
    avg_degree = round(np.mean(list(dict(g.degree).values())),2)
    try:
        diameter = nx.diameter(nx.Graph(g))
    except Exception as e:
        diameter = e#f"{type(e).__name__}: {e}"
    try:
        radius  = nx.radius(g)
    except Exception as e:
        radius = e
    try:
        avg_geo_distance = round(nx.average_shortest_path_length(g,weight='weight'),2)
    except Exception as e:
        avg_geo_distance = e
    try:
        reciprocity = nx.overall_reciprocity(g)
    except Exception as e:
        reciprocity = e
    try:
        clustering_coef = nx.average_clustering(g)
    except Exception as e:
        clustering_coef = e
    try:
        transitivity = nx.transitivity(g)
    except Exception as e:
        transitivity = e
    try:
        flow_hierarchy = nx.flow_hierarchy(g,weight='weight')
    except Exception as e:
        try:
            flow_hierarchy = flow_hierarchy = nx.flow_hierarchy(g)
        except Exception as e:
            flow_hierarchy = e


    d_temp = pd.DataFrame({
                            '#edges':[num_edges],
                            '#nodes':[num_nodes],
                            'density':[density],
                            'diameter':[diameter],
                            'radius':[radius],
                            'avg_geo_distance':[avg_geo_distance],
                            'avg_degree':[avg_degree],
                            'reciprocity':[reciprocity],
                            'clustering_coef':[clustering_coef],
                            'transitivity':[transitivity],
                            'flow_hierarchy':[flow_hierarchy]
                            },
                        index=[variable_name])
    d = pd.concat([d,d_temp])
display(pd.DataFrame(d))
