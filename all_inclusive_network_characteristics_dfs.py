import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import networkx.generators.small
import numpy as np
from datetime import datetime

#*********************************************
def centrality(edgelist_df,nodes,start_date_dict,period_in_days,timestamp__col_name,graph_name=None,ego_graph_radius=1):
    #g = graph
    #if graph_name == None:
    #    graph_name = g.name
    #if nodes == 'all':
    #    nodes = g.nodes
    dataframe = pd.DataFrame()
    for n in nodes:
        date_range = pd.date_range(start=start_date[n], periods=period_in_days)
        b = edgelist_df[timestamp_col_name].isin(date_range)
        g = nx.from_pandas_edgelist(edgelist_df.loc[b], source='source', target='target', edge_attr='timestamp', create_using=nx.MultiDiGraph, edge_key=None)
                
        ego_g = nx.ego_graph(g,n,radius=ego_graph_radius,center=True,undirected=False,distance=None) #For directed graphs D this produces the “out” neighborhood or successors. If you want the neighborhood of predecessors first reverse the graph with D.reverse(). If you want both directions use the keyword argument undirected=True.
        
        #size
        size1 = nx.ego_graph(g,n,radius=1).number_of_nodes() - 1
        size2 = nx.ego_graph(g,n,radius=2).number_of_nodes() - 1
        effective_size_ = nx.effective_size(g,nodes=[n],weight=None)[n]
        k_core_size = nx.k_core(ego_g, k=None, core_number=None).number_of_nodes() - 1
        
        #communication volume
        degree_centrality = g.degree(n) #nx.degree(ego_g,nbunch=n,weight=None)
        out_degree_cent = nx.out_degree_centrality(ego_g)[n]
        in_degree_cent = nx.in_degree_centrality(ego_g)[n]
        density = nx.density(ego_g)
        reciprocity_ = nx.reciprocity(ego_g,nodes=n)

        #efficiency
        Burts_efficiency = esize/g.degree(n)
        local_efficiency_ = local_efficiency(ego_g)

        #brokerage
        betweenness = nx.betweenness_centrality(g, k=None, normalized=True, weight=None, endpoints=False, seed=None)[n]
        constraint_ = nx.constraint(g, nodes=[n], weight=None)[n]
        info_cent = nx.information_centrality(nx.Graph(g), weight=None, dtype='float', solver='lu')[0]
        communicability_betweenness = nx.communicability_betweenness_centrality(nx.Graph(g))[n]
        
        #embeddedness
        triangles_cnt =  nx.triangles(g, nodes=[n]) #local_clustering_coefficient = nx.clustering(g, nodes=[n], weight=None)[n]
        closeness = nx.closeness_centrality(g, u=n, distance=None, wf_improved=True)
        harmonic_cent = nx.harmonic_centrality(g, nbunch=[n], distance=None, sources=None)[n]
        
        #reach
        eccentricity_ = nx.eccentricity(g, v=n, sp=None)
        local_reaching_centrality_ = local_reaching_centrality(g,n, paths=None, weight=None, normalized=True)
        
        #connectedness
        eigenvector_cent = nx.eigenvector_centrality(g, max_iter=100, tol=1e-06, nstart=None, weight=None)[n]
        second_order_cent = nx.second_order_centrality(nx.Graph(g)) #Lower values of second order centrality indicate higher centrality.
        PageRank = pagerank(g, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight', dangling=None)[n]

        temp_df = pd.DataFrame({
             'graph':graph_name
            ,'size1':size1
            ,'size2':size2
            ,'effective_size':effective_size_
            ,'k_core_size':k_core_size
            ,"Burt's efficiency":Burts_efficiency
            ,'local_efficiency':local_efficiency_
            ,'degree_centrality':degree_centrality
            ,'out_degree_cent':out_degree_cent
            ,'in_degree_cent':in_degree_cent
            ,'density':density
            ,'reciprocity':reciprocity_
            
            
            'node':dc.keys(),
            'degree':dc.values(),
            'betweenness': bc.values(),
            'closeness':cc.values(),
            'eigenvector':ec.values(),
            'PageRank':pr.values(),
            'lcc':lcc.values()
            })
        dataframe = pd.concat([dataframe,temp_df])
    return temp_df
#*********************************************
def ego_network_diversity(graph,attributes_df,node_col_name,attribute_col_name,graph_name=None,nodes='all',ego_graph_radius=1,use_k_core=False):
    g = graph
    if graph_name == None:
        graph_name = g.name
    if nodes == 'all':
        nodes = g.nodes    
    
    dataframe = pd.DataFrame()
    for n in nodes:
        ego_g = nx.ego_graph(g,n,radius=ego_graph_radius,center=True,undirected=False,distance=None) #For directed graphs D this produces the “out” neighborhood or successors. If you want the neighborhood of predecessors first reverse the graph with D.reverse(). If you want both directions use the keyword argument undirected=True.
        if use_k_core:
            ego_g = nx.k_core(ego_g,k=None,core_number=None)
        b = attributes_df[node_col_name].isin(ego_g.nodes)
        temp_df = attributes_df.loc[b,[attribute_col_name,node_col_name]].groupby(attribute_col_name).count()
        temp_df['node'] = n
        temp_df['assortativity'] = attribute_assortativity_coefficient(ego_g, attribute=attribute_col_name, nodes=None)
        temp_df = temp_df.reset_index().set_index(['node',c,'assortativity'])
        
        dataframe = pd.concat([dataframe,temp_df])
    return dataframe
    