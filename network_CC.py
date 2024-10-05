import networkx as nx


def compute_transitivity_from_gexf(file_path):
    # Caricamento del file GEXF nella rete
    G = nx.read_gexf(file_path)

    # Calcolo della transitività
    transitivity = nx.transitivity(G)

    return transitivity


def compute_reciprocity_from_gexf(file_path):
    G = nx.read_gexf(file_path)
    reciprocity = nx.reciprocity(G)

    return reciprocity


# Uso della funzione
# file_path = "network_visual_2.gexf"  # Sostituisci con il percorso al tuo file GEXF
# file_path = "network_v4.gexf"
file_path = "network_noobs.gexf"
result = compute_transitivity_from_gexf(file_path)
result_2 = compute_reciprocity_from_gexf(file_path)
print(f"Transitività: {result:.4f}")
print(f"Reciprocità: {result_2:.4f}")


import networkx as nx
import numpy as np

# Caricamento del file GEXF nella rete
# G = nx.read_gexf("network_visual_2_noLeaf.gexf")
# G = nx.read_gexf("network_v4.gexf")
G = nx.read_gexf("network_noobs.gexf")

# Estrazione degli attributi "rank" dai nodi
ranks = nx.get_node_attributes(G, "rank")

# Creazione di un set unico di valori di "rank"
unique_ranks = set(ranks.values())

# Calcolo di reciprocità e transitività per ogni valore di "rank"
results = {}
for rank in unique_ranks:
    subgraph_nodes = [node for node, rank_value in ranks.items() if rank_value == rank]
    subgraph = G.subgraph(subgraph_nodes)

    # Controllo se la sotto-rete è vuota
    if len(subgraph) == 0:
        reciprocity_value = np.nan
        transitivity_value = np.nan
    else:
        try:
            reciprocity_value = nx.reciprocity(subgraph)
        except:
            reciprocity_value = np.nan

        try:
            transitivity_value = nx.transitivity(subgraph)
        except:
            transitivity_value = np.nan

    results[rank] = {
        "Reciprocità": reciprocity_value,
        "Transitività": transitivity_value,
    }

# Presentazione dei risultati in forma tabellare
print(
    "| Rank         | Reciprocità                            | Transitività                             |"
)
print(
    "|--------------|---------------------------------------|-----------------------------------------|"
)
for rank, values in results.items():
    print(
        f"| {rank:12} | {values['Reciprocità']*100:.3f}%                                | {values['Transitività']*100:.3f}%                                    |"
    )
