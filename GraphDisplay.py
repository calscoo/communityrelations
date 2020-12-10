import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab


def get_color(i, r_off=1, g_off=1, b_off=1):
    '''Assign a color to a vertex.'''
    r0, g0, b0 = 0, 0, 0
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 3) % n) / (n - 1)
    g = low + span * (((i + g_off) * 5) % n) / (n - 1)
    b = low + span * (((i + b_off) * 7) % n) / (n - 1)
    return (r, g, b)


def generate_communities_graph(G, community_neighbor_relationships):

    node_color = [get_color(G.nodes[v]['community']) for v in G.nodes]

    # Set community color for edges between members of the same community (internal) and intra-community edges (external)
    external = [(v, w) for v, w in G.edges if G.edges[v, w]['community'] == 0]
    internal = [(v, w) for v, w in G.edges if G.edges[v, w]['community'] > 0]
    internal_color = ['black' for e in internal]
    related_community_edges = []
    for rel in community_neighbor_relationships.values():
        for pair in rel:
            related_community_edges.append(pair)
    unrelated_community_edges_set = set(external) - set(related_community_edges)
    unrelated_community_edges = list(unrelated_community_edges_set)

    pos = nx.spring_layout(G)

    plt.rcParams.update({'figure.figsize': (15, 10)})
    # Draw unrelated_community_edges
    nx.draw_networkx(
        G,
        pos=pos,
        node_size=0,
        edgelist=unrelated_community_edges,
        edge_color="silver")
    # Draw related_community_edges
    nx.draw_networkx(
        G,
        pos=pos,
        node_size=0,
        edgelist=related_community_edges,
        edge_color="red",
        width=5)
    # Draw nodes and internal edges
    nx.draw_networkx(
        G,
        pos=pos,
        node_color=node_color,
        edgelist=internal,
        edge_color=internal_color)

    plt.show()


def save_graph(graph, file_name):
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos)

    plt.savefig(file_name, bbox_inches="tight")
    pylab.close()
    del fig
