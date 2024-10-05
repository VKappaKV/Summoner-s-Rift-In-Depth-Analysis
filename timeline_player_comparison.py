from riotwatcher import LolWatcher, ApiError
import json
import matplotlib.pyplot as plt

lol_watcher = LolWatcher("RGAPI-bf368394-08e9-4fe4-becc-59034b2063c4")


def get_match_timeline(match):
    try:
        return lol_watcher.match.timeline_by_match("euw1", match)
    except ApiError as err:
        if err.response.status_code == 429:
            print("We should retry in {} seconds.".format(err.headers["Retry-After"]))
            return get_match_timeline(match)
        else:
            return None


""" timeline_data = get_match_timeline("EUW1_6518435385")
with open("tryout_timeline2.json", "w") as p:
    json.dump(timeline_data, p, indent=4)
 """
with open("tryout_timeline.json", "r") as t:
    timeline_data = json.load(t)


def extract_performance_updated(player_id1, player_id2, data):
    """
    Estrae le performance dei giocatori durante la partita con ulteriori correzioni.

    Args:
    - player_id1 (int): ID del primo giocatore.
    - player_id2 (int): ID del secondo giocatore.
    - data (dict): Dati del JSON.

    Returns:
    - dict: Un dizionario con le performance dei giocatori.
    """
    player1_data = {"gold": [], "cs": [], "exp": []}
    player2_data = {"gold": [], "cs": [], "exp": []}

    # Estrai le performance dai frames
    for frame in data["info"]["frames"]:
        p1_frame = frame["participantFrames"].get(str(player_id1))
        p2_frame = frame["participantFrames"].get(str(player_id2))

        if p1_frame:
            player1_data["gold"].append(p1_frame["totalGold"])  # Corretto a 'totalGold'
            player1_data["cs"].append(p1_frame["jungleMinionsKilled"])
            player1_data["exp"].append(p1_frame.get("xp", 0))

        if p2_frame:
            player2_data["gold"].append(p2_frame["totalGold"])  # Corretto a 'totalGold'
            player2_data["cs"].append(p2_frame["jungleMinionsKilled"])
            player2_data["exp"].append(p2_frame.get("xp", 0))

    return player1_data, player2_data


def plot_comparison(player1_data, player2_data, player_id1, player_id2):
    metrics = ["gold", "cs", "exp"]
    titles = ["Gold over Time", "CS (Creep Score) over Time", "Experience over Time"]

    # Crea i grafici
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    for i, metric in enumerate(metrics):
        axs[i].plot(player1_data[metric], label=f"KhaZix")
        axs[i].plot(player2_data[metric], label=f"Nidalee")
        axs[i].set_title(titles[i])
        axs[i].set_xlabel("")
        axs[i].set_ylabel(metric.capitalize())
        axs[i].legend()

    plt.tight_layout()
    plt.show()


# Estraiamo nuovamente le performance dei giocatori con ID 1 e 6 usando la funzione aggiornata
player1_data_updated, player2_data_updated = extract_performance_updated(
    2, 7, timeline_data
)
plot_comparison(player1_data_updated, player2_data_updated, 2, 7)
