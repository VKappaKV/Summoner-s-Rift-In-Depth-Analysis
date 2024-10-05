import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

with open("jungler_network_pros.json", "r") as f:
    data = json.load(f)
    print(len(data.keys()))

G = nx.read_gexf("network_v4.gexf")
with open("jungler_network_noobs.json", "r") as f:
    data = json.load(f)
    print(len(data.keys()))

G = nx.read_gexf("network_noobs.gexf")

num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print(num_nodes, " - ", num_edges)

degree = dict(G.degree())
massimo = max(degree.items(), key=lambda x: x[1])[0]
print(massimo)

degree_list = list(degree.values())

print(f"Grado medio: {np.mean(degree_list)}")
print(f"Standard deviation: {np.std(degree_list)}")
print(f"Median: {np.median(degree_list)}")
print(f"Min: {np.min(degree_list)}")
print(f"Max: {np.max(degree_list)}")


hub = np.percentile(degree_list, 50)
hub_tpl = (
    np.percentile(degree_list, 80, method="lower"),
    np.percentile(degree_list, 80, method="midpoint"),
    np.percentile(degree_list, 80, method="higher"),
)
print(hub, " tuple: ", hub_tpl)

from matplotlib.colors import LogNorm

games_played = {node: G.in_degree(node) + G.out_degree(node) for node in G.nodes}
win_loss_ratio = {
    node: G.out_degree(node) / games_played[node] if games_played[node] != 0 else 0
    for node in G.nodes
}
# Codice per games_played e win_loss_ratio (già fornito)
x = list(games_played.values())
y = list(win_loss_ratio.values())


midpoint_x = (max(x) + min(x)) / 2

# Calcola il valore y corrispondente al 50% per il rapporto W/L
midpoint_y = 0.5

# Calcola il conteggio delle occorrenze di ciascun valore di x e y
x_counts = {val: x.count(val) for val in set(x)}
y_counts = {val: y.count(val) for val in set(y)}

# Combina i conteggi di x e y per ottenere il gradiente
combined_counts = [x_counts.get(val, 0) + y_counts.get(val, 0) for val in x]

# Trova il numero massimo di nodi per la corretta scala dei colori
max_nodes_count = max(combined_counts)

# Crea il diagramma
plt.figure(figsize=(8, 6))

# Traccia i punti con gradiente basato sulla combinazione di x e y
norm = LogNorm(vmin=1, vmax=max_nodes_count)
sc = plt.scatter(
    x, y, c=combined_counts, s=combined_counts, cmap="viridis", norm=norm, alpha=0.7
)

# Aggiungi una colorbar per mostrare la scala dei colori
cbar = plt.colorbar(sc)
cbar.set_label("Numero di nodi")
cbar.ax.yaxis.set_tick_params(pad=8)  # Aumenta lo spazio tra i tick e l'etichetta

# Etichette per la colorbar
cbar.ax.set_yticklabels([f"{int(tick):,}" for tick in cbar.get_ticks()])
cbar.ax.text(
    1.1,
    0.5,
    f"Scala utilizzata da 1 a {max_nodes_count:,}",
    transform=cbar.ax.transAxes,
    rotation=-90,
    va="center",
)

# Traccia la linea verticale perpendicolare all'asse delle x
plt.axvline(x=midpoint_x, color="red", linestyle="--")

# Traccia la linea orizzontale perpendicolare all'asse y
plt.axhline(y=midpoint_y, color="blue", linestyle="--")

# Etichette per le linee
plt.text(
    midpoint_x + 10,
    max(y),
    f"",
    color="red",
)
plt.text(max(x), midpoint_y + 0.01, "", color="blue")

plt.xlabel("Numero di partite giocate")
plt.ylabel("Rapporto W/L")
plt.title("Grafo WR/ # matches")
plt.grid(True)
# plt.show()
