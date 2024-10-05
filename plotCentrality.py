import networkx as nx
import matplotlib.pyplot as plt

# Crea un grafo di esempio (puoi sostituire con il tuo grafo)
file_path = "network_v4.gexf"
G = nx.read_gexf(file_path)

# Calcola le centralità
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)


# Funzione per visualizzare la distribuzione delle centralità
def plot_centrality_distribution(centrality_values, title):
    plt.hist(centrality_values, bins=50)
    plt.title(title)
    plt.ylabel("Number of Nodes")
    plt.xlabel("Centrality Value")

    plt.show()


# Visualizza la distribuzione delle centralità
plot_centrality_distribution(
    degree_centrality.values(), "Degree Centrality Distribution"
)
plot_centrality_distribution(
    betweenness_centrality.values(), "Betweenness Centrality Distribution"
)
plot_centrality_distribution(
    closeness_centrality.values(), "Closeness Centrality Distribution"
)
plot_centrality_distribution(
    eigenvector_centrality.values(), "Eigenvector Centrality Distribution"
)
