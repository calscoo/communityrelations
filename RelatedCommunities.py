import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab
import numpy as np

def set_node_community(G, communities):
    '''Add community to node attributes'''
    for c, v_c in enumerate(communities):
        for v in v_c:
            # Add 1 to save 0 for external edges
            G.nodes[v]['community'] = c + 1


def set_edge_community(G):
    '''Find internal edges and add their community to their attributes'''
    for v, w, in G.edges:
        if G.nodes[v]['community'] == G.nodes[w]['community']:
            # Internal edge, mark with community
            G.edges[v, w]['community'] = G.nodes[v]['community']
        else:
            # External edge, mark as 0
            G.edges[v, w]['community'] = 0


def detect_related_communities(G, communities, relation_strength):
    set_node_community(G, communities)
    set_edge_community(G)

    # Set community color for edges between members of the same community (internal) and intra-community edges (external_edges)
    external_edges = [(v, w) for v, w in G.edges if G.edges[v, w]['community'] == 0]

    related_community_edges = dict()

    for edge in external_edges:
        x = G.nodes[edge[0]]['community']
        y = G.nodes[edge[1]]['community']
        key = str(x) + "_" + str(y)
        temp = related_community_edges.get(key)
        edges = []
        if temp is not None:
            edges = temp
        del temp
        edges.append(edge)
        related_community_edges[key] = edges
        del edges

    dead_keys = set()
    for key in related_community_edges.keys():
        if key not in dead_keys:
            split = key.split("_")
            flipped = split[1] + "_" + split[0]
            temp = related_community_edges.get(flipped)
            if temp is not None:
                cur = related_community_edges.get(key)
                related_community_edges[key] = cur + temp
                del cur
                del temp
                dead_keys.add(flipped)

    for dead_key in dead_keys:
        del related_community_edges[dead_key]

    for rel in related_community_edges.values():
        used = set()
        dead_pairs = set()
        for pair in rel:
            x = pair[0]
            y = pair[1]
            if x in used or y in used:
                dead_pairs.add(pair)
            used.add(pair[0])
            used.add(pair[1])
        for dead_pair in dead_pairs:
            rel.remove(dead_pair)

    dead_keys = set()
    for key in related_community_edges:
        split = key.split("_")
        small_size = len(communities[int(split[0]) - 1])
        t = len(communities[int(split[0]) - 2])
        small_size = t if small_size > t else small_size
        relations_required = round(small_size * relation_strength)
        if related_community_edges.get(key).__len__() < relations_required:
            dead_keys.add(key)

    for dead_key in dead_keys:
        del related_community_edges[dead_key]

    return related_community_edges
