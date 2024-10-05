import json
from collections import defaultdict

# Carichiamo nuovamente il JSON
with open("jungler_network_noobs.json", "r") as f:
    data_fixed = json.load(f)

# Contiamo nuovamente i campioni più giocati da ciascun giocatore
champion_count_fixed = defaultdict(lambda: defaultdict(int))
for player, player_data in data_fixed.items():
    for match_list_key in ["OUT", "IN"]:
        if match_list_key in player_data:
            for match in player_data[match_list_key]:
                champion = match.get("champion")
                if champion:
                    champion_count_fixed[player][champion] += 1


def extract_player_info(player_id, data):
    player_data = data.get(player_id, {})
    if not player_data:
        return {"error": f"Giocatore {player_id} non trovato nel JSON."}

    # Estrai Rank, Tier e LP
    info = player_data.get("INFO", {})
    rank = info.get("rank", "N/A")
    tier = info.get("tier", "N/A")
    lp = info.get("LP", "N/A")

    # Estrai il numero totale di partite giocate
    out_matches = player_data.get("OUT", [])
    in_matches = player_data.get("IN", [])
    total_matches = len(out_matches) + len(in_matches)

    # Estrai il campione preferito
    most_played_champion = max(
        champion_count_fixed[player_id],
        key=champion_count_fixed[player_id].get,
        default="N/A",
    )

    return {
        "Rank": rank,
        "Tier": tier,
        "LP": lp,
        "Total Matches": total_matches,
        "Most Played Champion": most_played_champion,
    }


# Testiamo nuovamente lo script con il giocatore "LuvFlakkedCheeks"
example_output = extract_player_info("STAND NAME", data_fixed)
print(example_output)
