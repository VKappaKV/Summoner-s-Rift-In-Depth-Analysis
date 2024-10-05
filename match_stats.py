import json
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from collections import defaultdict

""" with open('jungler_network_pros.json','r') as p:
    data = json.load(p) """
with open("jungler_network_noobs.json", "r") as p:
    data = json.load(p)

import requests


def get_champion_name_from_id(champion_id):
    # URL dell'endpoint dell'API di Riot Games per ottenere i dettagli dei campioni
    url = "https://ddragon.leagueoflegends.com/cdn/11.3.1/data/en_US/champion.json"

    response = requests.get(url)
    data = response.json()

    # Ricerca del nome del campione usando l'ID
    for champ, details in data["data"].items():
        if details["key"] == str(champion_id):
            return champ

    return None


def timestamp_to_min(timestamp_in_secondi):
    minuti = timestamp_in_secondi // 60
    secondi = timestamp_in_secondi % 60
    formato_mm_ss = "{:02d}:{:02d}".format(int(minuti), int(secondi))
    return minuti


def timestamp_to_datetime(timestamp_ms):
    timestamp_seconds = timestamp_ms / 1000
    dt_object = datetime.fromtimestamp(timestamp_seconds)
    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


average_duration = 0
count_match = 0

timestamps_list = []


for player, player_data in data.items():
    for match in player_data["OUT"]:
        duration = match["info"]["gameDuration"]
        timestamp = match["info"]["gameStartTimestamp"]
        timestamps_list.append(timestamp / 1000)
        average_duration += duration
        count_match += 1
    for match in player_data["IN"]:
        duration = match["info"]["gameDuration"]
        timestamp = match["info"]["gameStartTimestamp"]
        timestamps_list.append(timestamp / 1000)
        average_duration += duration
        count_match += 1
average_duration = average_duration / count_match

# Crea una lista di oggetti datetime dai timestamp
datetimes_list = [datetime.fromtimestamp(timestamp) for timestamp in timestamps_list]

# Dizionari per contare il numero di picks e bans per ogni campione
champion_picks = defaultdict(int)
champion_bans = defaultdict(int)
matches = set()

# Scansione dei dati per contare picks e bans
for player, player_data in data.items():
    for match_type in ["OUT", "IN"]:
        for match in player_data.get(match_type, []):
            # Estrazione dell'ID del match
            matches.add(match["matchID"])

            # Conteggio dei picks
            champion_picks[match["champion"]] += 1
            champion_picks[match["vsChampion"]] += 1

            # Conteggio dei bans
            for banned_champion in match["bans"]:
                champion_bans[banned_champion] += 1
            for banned_champion in match["vs_bans"]:
                champion_bans[banned_champion] += 1

# Calcolo del totale delle partite
total_matches = len(matches)

# Calcolo dei pick rate e ban rate
pick_rates = {
    champ: (count / total_matches) * 100 for champ, count in champion_picks.items()
}
ban_rates = {
    champ: (count / total_matches) * 100 for champ, count in champion_bans.items()
}

# Calcolo della somma di pick rate e ban rate
combined_rates = {
    champ: pick_rates.get(champ, 0) + ban_rates.get(champ, 0)
    for champ in set(champion_picks) | set(champion_bans)
}

played_champions = set(champion_picks.keys())

# Filtraggio dei combined_rates per includere solo i campioni giocati
filtered_combined_rates = {
    champ: rate
    for champ, rate in combined_rates.items()
    if get_champion_name_from_id(champ) in played_champions
}

# Ordinamento dei campioni in base alla somma di pick rate e ban rate tra i campioni giocati
sorted_filtered_combined_rates = sorted(
    filtered_combined_rates.items(), key=lambda x: x[1], reverse=True
)

for elem_combined in sorted_filtered_combined_rates[:10]:
    elem = elem_combined[0]
    print(
        get_champion_name_from_id(elem),
        " -- ",
        pick_rates[get_champion_name_from_id(elem)],
        "--",
        ban_rates[elem],
    )


def aggiungi_campioni(dizionario, lista_campioni):
    for campione in lista_campioni:
        if campione in dizionario:
            dizionario[campione] += 1
        else:
            dizionario[campione] = 1
    return dizionario


def extract_most_banned_champions_from_json(file_path):
    # Caricamento del file JSON
    with open(file_path, "r") as f:
        data = json.load(f)

    # Estrazione degli attributi dei nodi
    bans = {}
    for player, player_data in data.items():
        for match in player_data["OUT"]:
            player_bans = match["bans"]
            avversary_bans = match["vs_bans"]
            match_bans = list(set(player_bans) | set(avversary_bans))
            bans = aggiungi_campioni(bans, match_bans)
        for match in player_data["IN"]:
            player_bans = match["bans"]
            avversary_bans = match["vs_bans"]
            match_bans = player_bans + avversary_bans
            bans = aggiungi_campioni(bans, match_bans)

    # Ordinamento degli ID dei campioni in base al numero di volte in cui sono stati bannati
    sorted_bans = sorted(bans.items(), key=lambda x: x[1], reverse=True)

    return sorted_bans


# Uso della funzione
# file_path = "jungler_network_2.json"
file_path = "jungler_network_noobs.json"
most_banned_champions = extract_most_banned_champions_from_json(file_path)


def top_10_banned_champions(sorted_bans):
    # Estrai i primi 10 campioni più bannati
    top_10_bans = sorted_bans[:10]

    result = []
    for champion_id, bans in top_10_bans:
        champion_name = get_champion_name_from_id(champion_id)
        percentage = (bans / total_matches) * 100
        result.append((champion_id, champion_name, bans, percentage, total_matches))

    return result


top_10_champions = top_10_banned_champions(most_banned_champions)
for champion in top_10_champions:
    print(
        f"{champion[0]}: {champion[1]} -> {champion[2]} bans ({champion[3]:.2f}%) in {champion[4]} matches"
    )


target = 107
target_bans = []

# Scansione dei dati per trovare quando e da chi è stato bannato Rengar
for player, player_data in data.items():
    for match in player_data["OUT"]:
        if target in match["bans"]:
            target_bans.append(
                {"player": player, "champion": match["champion"], "banned_by": "player"}
            )
        if target in match["vs_bans"]:
            target_bans.append(
                {
                    "player": player,
                    "champion": match["vsChampion"],
                    "banned_by": "opponent",
                }
            )

    for match in player_data["IN"]:
        if target in match["bans"]:
            target_bans.append(
                {"player": player, "champion": match["champion"], "banned_by": "player"}
            )
        if target in match["vs_bans"]:
            target_bans.append(
                {
                    "player": player,
                    "champion": match["vsChampion"],
                    "banned_by": "opponent",
                }
            )

target_bans_analysis_v4 = []

# Scansione dei dati per trovare quando e da chi è stato bannato Rengar
for player, player_data in data.items():
    # Controllo l'esistenza del campo 'INFO' e successivamente dei campi 'tier' e 'rank'
    player_info = player_data.get("INFO") or {}
    player_rank = player_info.get("tier", "Unknown")

    for match in player_data.get("OUT", []):
        if target in match["bans"]:
            target_bans_analysis_v4.append(
                {
                    "player": player,
                    "champion": match["champion"],
                    "banned_by": "player",
                    "rank": player_rank,
                }
            )
        if target in match["vs_bans"]:
            target_bans_analysis_v4.append(
                {
                    "player": player,
                    "champion": match["vsChampion"],
                    "banned_by": "opponent",
                    "rank": player_rank,
                }
            )

    for match in player_data.get("IN", []):
        if target in match["bans"]:
            target_bans_analysis_v4.append(
                {
                    "player": player,
                    "champion": match["champion"],
                    "banned_by": "player",
                    "rank": player_rank,
                }
            )
        if target in match["vs_bans"]:
            target_bans_analysis_v4.append(
                {
                    "player": player,
                    "champion": match["vsChampion"],
                    "banned_by": "opponent",
                    "rank": player_rank,
                }
            )

target_bans_analysis_v4[:10]


# Creazione di un dizionario per contare l'occorrenza di ciascun campione nelle partite in cui Rengar è stato bannato
champion_correlation = defaultdict(int)

for entry in target_bans_analysis_v4:
    champion_correlation[entry["champion"]] += 1

# Ordinamento dei campioni in base al numero di volte in cui sono apparsi
sorted_champions = sorted(
    champion_correlation.items(), key=lambda x: x[1], reverse=True
)
print(sorted_champions[:10])  # Mostra i primi 10 campioni più frequenti
# Dizionari per contare il numero di picks e bans per ogni campione
champion_picks = defaultdict(int)
champion_bans = defaultdict(int)
matches = set()

# Scansione dei dati per contare picks e bans
for player, player_data in data.items():
    for match_type in ["OUT", "IN"]:
        for match in player_data.get(match_type, []):
            # Estrazione dell'ID del match
            match_id = list(match.keys())[0]
            matches.add(match_id)

            # Conteggio dei picks
            champion_picks[match["champion"]] += 1
            champion_picks[match["vsChampion"]] += 1

            # Conteggio dei bans
            for banned_champion in match["bans"]:
                champion_bans[banned_champion] += 1
            for banned_champion in match["vs_bans"]:
                champion_bans[banned_champion] += 1

# Calcolo del totale delle partite
total_matches = len(matches)

# Calcolo dei pick rate e ban rate
pick_rates = {
    champ: (count / total_matches) * 100 for champ, count in champion_picks.items()
}
ban_rates = {
    champ: (count / total_matches) * 100 for champ, count in champion_bans.items()
}

# Calcolo della somma di pick rate e ban rate
combined_rates = {
    champ: pick_rates.get(champ, 0) + ban_rates.get(champ, 0)
    for champ in set(champion_picks) | set(champion_bans)
}

# Ordinamento dei campioni in base alla somma di pick rate e ban rate
sorted_combined_rates = sorted(pick_rates.items(), key=lambda x: x[1], reverse=True)
sorted_combined_rates = sorted(ban_rates.items(), key=lambda x: x[1], reverse=True)
sorted_combined_rates = sorted(combined_rates.items(), key=lambda x: x[1], reverse=True)
