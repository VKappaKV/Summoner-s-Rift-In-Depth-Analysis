import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Creazione del grafo (sostituisci con la tua definizione)
# G = nx.read_gexf("network_visual_2.gexf")


# GRAFO SENZA NODI FOGLIA

"""
print(G.number_of_nodes(), ' --- ', G.number_of_edges())

# ... Aggiungi i nodi e gli archi al grafo ...

# Trova i nodi foglia
leaf_nodes = [node for node, degree in G.degree() if degree == 1 and degree == 0]

# Rimuovi i nodi foglia dal grafo
G.remove_nodes_from(leaf_nodes)
print('nodi foglia rimossi: ', len(leaf_nodes))
print(G.number_of_nodes(), ' --- ', G.number_of_edges())

nx.write_gexf(G, 'network_visual_noLeaf.gexf') """

with open("jungler_network_noobs.json", "r") as p:
    data = json.load(p)

champions_w = {}
champions_l = {}
ban_count = {}
for player, player_data in data.items():
    for match in player_data["OUT"]:
        champion_won = match["champion"]
        champion_lost = match["vsChampion"]
        champions_w[champion_won] = champions_w.get(champion_won, 0) + 1
        champions_l[champion_lost] = champions_l.get(champion_lost, 0) + 1
    for match in player_data["IN"]:
        champion_won = match["vsChampion"]
        champion_lost = match["champion"]
        champions_w[champion_won] = champions_w.get(champion_won, 0) + 1
        champions_l[champion_lost] = champions_l.get(champion_lost, 0) + 1


all_champions = champions_w.copy()
all_champions.update(champions_l)

# Calcola i rapporti
rapporti = {
    champion: champions_w.get(champion, 0)
    / (champions_w.get(champion, 0) + champions_l.get(champion, 0))
    for champion in all_champions
}

# Creazione del DataFrame con i dati
data = {
    "Vittorie": [champions_w.get(champion, 0) for champion in all_champions],
    "Sconfitte": [champions_l.get(champion, 0) for champion in all_champions],
    "Match": [
        champions_w.get(champion, 0) + champions_l.get(champion, 0)
        for champion in all_champions
    ],
    "Rapporto %": [rapporti[champion] for champion in all_champions],
    "Campione": [champion for champion in all_champions],
}

df = pd.DataFrame(data, index=all_champions)
df_sorted = df.sort_values(by="Vittorie", ascending=False)

file_path = "visualizzazioniNoobs/output.xlsx"  # Specifica il percorso del file Excel
df_sorted.to_excel(file_path, index=False)

df_sorted = df_sorted.query("(Vittorie + Sconfitte) >= 5")

colors = [
    random.choice(
        ["red", "blue", "green", "purple", "orange", "yellow", "pink", "cyan"]
    )
    for _ in range(len(df))
]
top_5_played = df_sorted.nlargest(5, "Vittorie")["Campione"].tolist()
best_wr_champions = df_sorted.nlargest(5, "Rapporto %")["Campione"].tolist()


colors = []
# labels = ['Rek\'Sai','Fiddlestick','Kha\'Zix','Evelynn','Kindred','Jarvan IV', 'Nunu & Willump', 'Ivern', 'Volibear','Rumble','Nidalee','Udyr','Graves','Lilia','Maokai','Viego']  # Lista per memorizzare i nomi dei campioni con requisiti specificati
for champion in df_sorted["Campione"]:
    if rapporti[champion] >= 0.50:
        colors.append("red")  # Dai un colore rosso ai campioni nella top 5 più giocati
    else:
        colors.append(
            "blue"
        )  # Altrimenti, usa il colore blu di default per gli altri campioni

# Creazione del diagramma a dispersione con i colori assegnati e le label
plt.figure(figsize=(10, 8))
plt.scatter(
    x=df_sorted["Vittorie"] + df_sorted["Sconfitte"],
    y=df_sorted["Rapporto %"],
    c=colors,
    marker="o",
)

for i in range(len(df)):
    plt.text(
        df["Vittorie"][i] + df["Sconfitte"][i] + 0.2,
        df["Rapporto %"][i],
        df["Campione"][i],
        fontsize=8,
    )

# Aggiungi etichette agli assi
plt.xlabel("Numero di partite giocate (vittorie + sconfitte)")
plt.ylabel("Rapporto W/L")
plt.title("Diagramma Rapporto W/L vs Partite Giocate")

# Mostra il diagramma
plt.grid(True)
plt.show()
