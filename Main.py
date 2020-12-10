import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.community as nxcom
import uuid
import GraphDisplay as graph_display
import RelatedCommunities as related_com

# data
basedir = "C:/Users/Caleb/PycharmProjects/school/datamining/communityrelations/datasets/"
git_data = basedir + "musae_git_edges.txt"
bio_data = basedir + "bio-diseasome.txt"
karate_data = basedir + "karate.txt"

DG = nx.read_edgelist(bio_data)
G = DG.to_undirected()
n = nx.number_of_nodes(G)

print("Show Graph")
# nx.draw(G, with_labels=False, node_size=50)
pos = nx.spring_layout(G)
nx.draw_networkx(
        G,
        node_size=10,
        with_labels=False,
        pos=pos,
        node_color="red",
        edgelist=G.edges,
        edge_color="black")
plt.show()

# calculate node degree
print("Node Degrees")
nodeDegrees = [val for (node, val) in G.degree()]
print(nodeDegrees)

# calculate degree frequency
print("Degree Frequencies")
degreeFrequencies = [0]*n
df = nx.degree_histogram(G)
for x in range(0, df.__len__()):
    degreeFrequencies[x] = df[x]
print(degreeFrequencies)

# calculate degree probabilities
print("Degree Probabilities")
degreeProbabilities = [0]*n
for x in range(0, n):
    degreeProbabilities[x] = round(degreeFrequencies[x]/n, 4)
print(degreeProbabilities)

# calculate clustering coefficients
print("Node Clustering Coefficients")
print(nx.clustering(G))

# calculate graph clustering coefficient
print("Graph Clustering Coefficient")
print(nx.average_clustering(G))

# plot degree frequencies
print("Plotting Degree Frequencies")
plt.hist(nodeDegrees, 100, color='purple', alpha=0.7)
plt.xlabel("Degree")
plt.ylabel("# of Nodes")
plt.xlim(0, 50)
plt.show()

# plot log scale degree probabilities
print("Plotting Log Scale Degree Probabilities")
for x in range(0, n):
    plt.scatter(x, degreeProbabilities[x], marker=".", color="k", s=150)
plt.xlabel("Node Degree (log)")
plt.ylabel("Probability of Having Degree (log)")
plt.loglog()
plt.show()

# calculate communities
print("Calculating Communities")
communities = nxcom.greedy_modularity_communities(G)
print(f"# of communities: {len(communities)}")
print(communities)

# detect neighbor communities
print("Detect Neighboring Communities")
related_community_edges = related_com.detect_related_communities(G, communities, 0.30)
print(f"# of community relations: {related_community_edges.__len__()}")
print(related_community_edges)

# generate graphs communities
print("Generating Communities Graph")
graph_display.generate_communities_graph(G, related_community_edges, False, False)
graph_display.generate_communities_graph(G, related_community_edges, True, False)
graph_display.save_graph(G, "graphs/my_graph_" + str(uuid.uuid4().hex) + ".pdf")
