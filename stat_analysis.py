import networkx as nx
import json

G = nx.read_gexf("network_v4.gexf")

with open("jungler_network_pros.json", "r") as f:
    data = json.load(f)

""" # Trova tutte le componenti connesse e identifica la componente gigante
giant_component = max(nx.strongly_connected_components(G), key=len)

# Crea un sottografo basato sulla componente gigante
G_giant = G.subgraph(giant_component)

# Calcola il diametro della componente gigante
diameter = nx.diameter(G_giant)

# print("Diametro della componente gigante:", diameter)
# pros: Diametro della componente gigante: 13
# noobs: Diametro della componente gigane: 10

# Calcola il clustering locale medio
avg_clustering = nx.average_clustering(G)

print("Clustering locale medio:", avg_clustering)

# Ottieni il coefficiente di clustering per ogni nodo
clustering_coeffs = nx.clustering(G)

# Filtra i nodi con coefficiente di clustering > 0
non_zero_clustering = [coeff for coeff in clustering_coeffs.values() if coeff > 0]

# Calcola il clustering medio per questi nodi, se esistono
if non_zero_clustering:
    avg_clustering_non_zero = sum(non_zero_clustering) / len(non_zero_clustering)
    print("Clustering medio per nodi con CC > 0:", avg_clustering_non_zero)

""" """
pros:
Clustering locale medio: 0.004734807926971433
Clustering medio per nodi con CC > 0: 0.03819827746026212
noobs:
Clustering locale medio: 2.9681061403995047e-05
Clustering medio per nodi con CC > 0: 0.033994708994708994
 """

""" lista = G.predecessors("FaithXD")
for l in lista:
    # if G.degree(l) > 10:
    # print(l, " :  : ", G.degree(l))
    print(l, " :  : ", G.degree(l))
 """
import pandas as pd

top5_EC = [
    ("Groinze", 0.17081319094397215),
    ("FaithXD", 0.15195576324537874),
    ("matrix agent 2", 0.13865007316096215),
    ("FA Warrior", 0.12801691617251587),
    ("Maître 0", 0.12096204634653036),
]
# Top nodi per Betweenness Centrality:
top5_betweenness = [
    ("Vedoluinim", 0.01613910864334569),
    ("HORSETOCHALL", 0.015428245174604035),
    ("Cochon à 8h", 0.015041498642427906),
    ("MetaSlaveJungler", 0.013992144581473036),
    ("Ciamajda", 0.013351049198755545),
]

# Top nodi per Closeness Centrality:
top5_closeness = [
    ("Bolshoi Booze", 0.18882996445900438),
    ("ME LittleLaudi", 0.18445959816266666),
    ("HORSETOCHALL", 0.18358052144386128),
    ("matrix agent 2", 0.18266165160523287),
    ("Villano Elmo", 0.1814071893501116),
]
# Top nodi per Degree Centrality:
top5_degree = [
    ("Vedoluinim", 0.010416666666666668),
    ("HORSETOCHALL", 0.00959967320261438),
    ("FA Warrior", 0.00959967320261438),
    ("Famous Fingers 5", 0.009191176470588236),
    ("PayzBack", 0.008986928104575164),
]


import pandas as pd
import matplotlib.pyplot as plt

# Estrai solamente i nomi dai dati
nodi_EC = [item[0] for item in top5_EC]
nodi_betweenness = [item[0] for item in top5_betweenness]
nodi_closeness = [item[0] for item in top5_closeness]
nodi_degree = [item[0] for item in top5_degree]

# Crea un DataFrame
df = pd.DataFrame(
    {
        "Eigenvector Centrality": nodi_EC,
        "Betweenness Centrality": nodi_betweenness,
        "Closeness Centrality": nodi_closeness,
        "Degree Centrality": nodi_degree,
    }
)

# Visualizza il DataFrame con matplotlib
fig, ax = plt.subplots(figsize=(10, 5))  # Imposta le dimensioni della figura
ax.axis("off")
ax.axis("tight")
tbl = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

# Stilizza la tabella
tbl.auto_set_font_size(False)
tbl.set_fontsize(12)
tbl.scale(1.2, 1.2)
for (i, j), cell in tbl.get_celld().items():
    if i == 0:
        cell.set_text_props(fontweight="bold", color="w")
        cell.set_facecolor("#40466e")  # colore dell'intestazione
    else:
        cell.set_facecolor("#f5f5f5")  # colore delle altre celle

plt.title("Top 5 giocatori per metrica di centralità", fontsize=15, fontweight="bold")

plt.show()

exit(1)
print(nx.density(G))
leaf_nodes = [
    node for node in G.nodes() if G.in_degree(node) == 1 and G.out_degree(node) == 0
]

print("nodi foglia : ", len(leaf_nodes))

generator_nodes = [node for node in G.nodes() if node in data.keys()]

tryharder_node = [node for node in generator_nodes if G.degree(node) > 5]

winning_nodes = [
    node for node in tryharder_node if G.out_degree(node) >= G.in_degree(node)
]
print(
    len(winning_nodes),
    " : ",
    len(data.keys()),
    " --- ",
    (len(winning_nodes) / len(data.keys())) * 100,
    "%",
)
# 462  :  1024  ---  45.1171875 %
# 413  :  995  ---  41.507537688442206 %
