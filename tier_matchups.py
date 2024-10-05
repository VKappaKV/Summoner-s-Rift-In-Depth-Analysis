import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

G = nx.read_gexf("network_noobs.gexf")
import matplotlib.pyplot as plt
import numpy as np

# Estrai tutti i rank unici dal grafo
unique_ranks = sorted(list(set(nx.get_node_attributes(G, "rank").values())))

# Crea una matrice di zeri delle dimensioni (numero di rank) x (numero di rank)
rank_matrix = np.zeros((len(unique_ranks), len(unique_ranks)))

# Popola la matrice con le occorrenze dei match
for edge in G.edges(data=True):
    source_rank = G.nodes[edge[0]]["rank"]
    target_rank = G.nodes[edge[1]]["rank"]
    rank_matrix[unique_ranks.index(source_rank)][
        unique_ranks.index(target_rank)
    ] += edge[2]["weight"]

# Calcola il totale di partite per ogni rank
total_games_per_rank = rank_matrix.sum(axis=1)

# Converti la matrice delle occorrenze in una matrice delle percentuali
percent_matrix = rank_matrix / total_games_per_rank[:, np.newaxis] * 100

# Visualizza la matrice con le percentuali
fig, ax = plt.subplots(figsize=(10, 10))
cax = ax.matshow(percent_matrix, cmap="gray_r")  # Usa una colormap in scala di grigi
plt.xticks(range(len(unique_ranks)), unique_ranks, rotation=45)
plt.yticks(range(len(unique_ranks)), unique_ranks)
plt.xlabel("Rank del nodo destinazione")
plt.ylabel("Rank del nodo sorgente")
plt.title("Matrice delle percentuali dei match tra rank")

# Aggiungi le percentuali come testo nelle celle
for i in range(len(unique_ranks)):
    for j in range(len(unique_ranks)):
        ax.text(
            j,
            i,
            f"{percent_matrix[i, j]:.2f}%",
            ha="center",
            va="center",
            color="black",
        )

plt.show()
