import networkx as nx
import json


def compute_centrality_metrics(file_path):
    # Caricamento del file GEXF nella rete
    G = nx.read_gexf(file_path)
    G_reverse = G.reverse()

    # Calcolo delle metriche di centralità
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G_reverse)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G_reverse)

    return (
        degree_centrality,
        closeness_centrality,
        betweenness_centrality,
        eigenvector_centrality,
    )


# Uso della funzione
# file_path = "network_visual_2.gexf"  # Sostituisci con il percorso al tuo file GEXF
file_path = "network_noobs.gexf"
file_path = "network_v4.gexf"
""" degree, closeness, betweenness, eigenvector = compute_centrality_metrics(file_path)

top5_degree = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:5]
top5_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:5]
top5_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
top5_EC = sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)[:5]
 """
G = nx.read_gexf(file_path)
# reversed_eigenvector = eigenvector_centrality = nx.eigenvector_centrality(G.reverse())
# top5_EC = sorted(reversed_eigenvector.items(), key=lambda x: x[1], reverse=True)[:5]
""" top5_degree = [
    ("Vedoluinim", 0.010416666666666668),
    ("HORSETOCHALL", 0.00959967320261438),
    ("FA Warrior", 0.00959967320261438),
    ("Famous Fingers 5", 0.009191176470588236),
    ("PayzBack", 0.008986928104575164),
]


top5_closeness = [
    ("iTaxz", 0.15286902222083656),
    ("Headbang Society", 0.15216620262817218),
    ("ever rising moon", 0.15131088784160895),
    ("HORSETOCHALL", 0.1509150229085505),
    ("Cochon à 8h", 0.15072349208440378),
]

top5_betweenness = [
    ("Vedoluinim", 0.01613910864334569),
    ("HORSETOCHALL", 0.015428245174604035),
    ("Cochon à 8h", 0.015041498642427906),
    ("MetaSlaveJungler", 0.013992144581473036),
    ("Ciamajda", 0.013351049198755545),
]

top5_EC = [
    ("FA Warrior", 0.14043196304316416),
    ("tent is back", 0.11708749583979881),
    ("matrix agent 2", 0.10539023673595896),
    ("Onîî", 0.1041925887557177),
    ("CALISTE CRIMINAL", 0.09855865620780768),
] """
###############################################################################################################################################
############################################################################################################################################################
################################################################################################################################################################################################################
############################################################################################################################################################
################################################################################################################################################################################################################
############################################################################################################################################################

# Top nodi per Eigenvector Centrality:
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


# Stampa dei nodi con i valori più alti per ciascuna metrica
print("Top nodi per Degree Centrality:")
print(top5_degree)
print("\nTop nodi per Closeness Centrality:")
print(top5_closeness)
print("\nTop nodi per Betweenness Centrality:")
print(top5_betweenness)
print("\nTop nodi per Eigenvector Centrality:")
print(top5_EC)


def get_node(node, graph, data):
    neighbors = list(graph.neighbors(node))
    # predecessors = list(graph.predecessors(node))
    details = {
        "node": node,
        "degree": graph.degree[node],
        "generator": node in data,
        "connected_nodes": [],
    }

    for neighbor in neighbors:
        neighbor_details = {
            "name": neighbor,
            "generator": neighbor in data,
            "out_degree": graph.out_degree(neighbor),
            "in_degree": graph.in_degree(neighbor),
            "rank": graph.nodes[neighbor].get("rank", None),
        }
        details["connected_nodes"].append(neighbor_details)

    return details


with open("jungler_network_pros.json", "r") as f:
    jungler_data = json.load(f)
G = nx.read_gexf(file_path)

details_degree = [get_node(node[0], G, jungler_data) for node in top5_degree]
details_betweeness = [get_node(node[0], G, jungler_data) for node in top5_betweenness]
details_EC = [get_node(node[0], G, jungler_data) for node in top5_EC]
details_closeness = [get_node(node[0], G, jungler_data) for node in top5_closeness]
with open("results_b.json", "w") as k:
    json.dump(details_betweeness, k, indent=4)
with open("results_ec.json", "w") as k:
    json.dump(details_EC, k, indent=4)
with open("results_c.json", "w") as k:
    json.dump(details_closeness, k, indent=4)
# FARE LA VISUALIZZAZIONE DEI GRAFI CONSIDERATI I CENTRI


def node_analysis(top_nodes):
    analysis = {}
    for node in top_nodes:
        # Generator vs Non-generator
        generator_count = sum(
            1 for item in node["connected_nodes"] if item["generator"]
        )
        non_generator_count = len(node["connected_nodes"]) - generator_count

        # Rank count
        rank_counts = {}
        for item in node["connected_nodes"]:
            if item["rank"]:
                rank_counts[item["rank"]] = rank_counts.get(item["rank"], 0) + 1

        # Out-degree and In-degree
        total_out_degree = sum(item["out_degree"] for item in node["connected_nodes"])
        total_in_degree = sum(item["in_degree"] for item in node["connected_nodes"])

        average_out_degree = total_out_degree / len(node["connected_nodes"])
        average_in_degree = total_in_degree / len(node["connected_nodes"])

        # Compile results
        analysis[node["node"]] = {
            "generator, non": (generator_count, non_generator_count),
            "rank counts": rank_counts,
            "node degree": node["degree"],
            "total degree": total_out_degree + total_in_degree,
            "total out degree": total_out_degree,
            "total in degree": total_in_degree,
            "average out degree": average_out_degree,
            "average in degree": average_in_degree,
        }

    return analysis


result_analysis_d = node_analysis(details_degree)
result_analysis_b = node_analysis(details_betweeness)
result_analysis_c = node_analysis(details_closeness)
result_analysis_ec = node_analysis(details_EC)

import pandas as pd


# Convert the analysis dictionary to a list of dictionaries format
def analysis_to_dataframe_format(analysis):
    rows = []
    for node, details in analysis.items():
        row = details.copy()
        row["node"] = node
        rows.append(row)
    return rows


df_format_d = analysis_to_dataframe_format(result_analysis_d)

# Create a dataframe from the list of dictionaries
df_d = pd.DataFrame(df_format_d)
# Convert the example data to dataframe format
df_format_b = analysis_to_dataframe_format(result_analysis_b)

# Create a dataframe from the list of dictionaries
df_b = pd.DataFrame(df_format_b)
# Convert the example data to dataframe format
df_format_c = analysis_to_dataframe_format(result_analysis_c)

# Create a dataframe from the list of dictionaries
df_c = pd.DataFrame(df_format_c)
# Convert the example data to dataframe format
df_format_ec = analysis_to_dataframe_format(result_analysis_ec)

# Create a dataframe from the list of dictionaries
df_ec = pd.DataFrame(df_format_ec)

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table


def save_dataframe_as_image(df, filename):
    fig, ax = plt.subplots(figsize=(12, len(df) * 0.5))
    ax.axis("off")
    tbl = table(
        ax, df, loc="center", cellLoc="center", colWidths=[0.15] * len(df.columns)
    )

    # Stima la larghezza in base alla lunghezza massima del contenuto
    rank_col_index = df.columns.get_loc("rank counts")
    max_content_length = max(df["rank counts"].apply(lambda x: len(str(x))))
    new_width = (
        max_content_length * 0.015
    )  # Riduci il fattore di scala per ridurre lo spazio bianco

    # Aggiusta la larghezza della colonna "rank counts"
    for i in range(len(df) + 1):
        tbl[(i, rank_col_index)].set_width(new_width)

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.2, 1.2)
    plt.subplots_adjust(left=0.2, top=1.2)
    plt.savefig(filename, bbox_inches="tight", dpi=300, pad_inches=0.5)


save_dataframe_as_image(df_d, "visualizzazioni/final/retry_tables_d.png")
save_dataframe_as_image(df_b, "visualizzazioni/final/retry_tables_b.png")
save_dataframe_as_image(df_c, "visualizzazioni/final/retry_tables_c.png")
save_dataframe_as_image(df_ec, "visualizzazioni/final/retry_tables_ec.png")
