import json
import networkx as nx
from collections import defaultdict

# Carichiamo il nuovo JSON modificato
with open("jungler_network_pros.json", "r") as f:
    data = json.load(f)

# Creiamo un nuovo grafo orientato
G = nx.DiGraph()


# Funzione per aggiungere un arco al grafo
def add_game_edge_new(G, player1, player2):
    if G.has_edge(player1, player2):
        G[player1][player2]["weight"] += 1
    else:
        G.add_edge(player1, player2, weight=1.0)


# Estraiamo nodi ed archi dal nuovo JSON
for player, player_data in data.items():
    if (
        player_data is not None
        and isinstance(player_data, dict)
        and "INFO" in player_data
        and player_data["INFO"] is not None
        and isinstance(player_data["INFO"], dict)
        and "tier" in player_data["INFO"]
    ):
        rank_v = player_data["INFO"]["tier"]
        G.add_node(player, rank=rank_v)

        # Partite "OUT" sono le vittorie
        for match in player_data["OUT"]:
            opponent = match["vs"]
            vs_queue_stats = match.get("vs_queue_stats", {})
            if vs_queue_stats and vs_queue_stats.get("tier"):
                stats = vs_queue_stats["tier"]
                G.add_node(opponent, rank=stats)
                add_game_edge_new(G, player, opponent)

        # Partite "IN" sono le sconfitte
        for match in player_data["IN"]:
            opponent = match["vs"]
            vs_queue_stats = match.get("vs_queue_stats", {})
            if vs_queue_stats and vs_queue_stats.get("tier"):
                stats = vs_queue_stats["tier"]
                G.add_node(opponent, rank=stats)
                add_game_edge_new(G, opponent, player)

# Dizionario per tenere traccia dei campioni giocati da ogni giocatore
champion_count_corrected = defaultdict(lambda: defaultdict(int))

# Iteriamo su tutti i giocatori nel JSON
for player, player_data in data.items():
    if player_data:
        # Contiamo i campioni giocati nelle partite "OUT"
        for match in player_data.get("OUT", []):
            champion = match.get("champion")
            if champion:
                champion_count_corrected[player][champion] += 1
            vs_champion = match.get("vsChampion")
            if vs_champion:
                champion_count_corrected[match["vs"]][vs_champion] += 1
        for match in player_data.get("IN", []):
            champion = match.get("champion")
            if champion:
                champion_count_corrected[player][champion] += 1
            vs_champion = match.get("vsChampion")
            if vs_champion:
                champion_count_corrected[match["vs"]][vs_champion] += 1

# Aggiungiamo l'attributo del campione più giocato a ogni nodo nel grafo
for player, champions in champion_count_corrected.items():
    # Troviamo il campione più giocato per ogni giocatore
    most_played_champion = max(champions, key=champions.get)
    if G.has_node(player):
        G.nodes[player]["most_played_champion"] = most_played_champion


# Ritorniamo il numero di nodi e archi nel nuovo grafo
num_nodes_new = G.number_of_nodes()
num_edges_new = G.number_of_edges()

print("modified", num_nodes_new, num_edges_new)
gexf_path = "network_v4.gexf"
# gexf_path = "network_noobs.gexf"
nx.write_gexf(G, gexf_path)
