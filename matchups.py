import json

""" with open('jungler_network_2.json','r') as p:
    data = json.load(p) """
with open("jungler_network_noobs.json", "r") as p:
    data = json.load(p)

matchups = {}

for player, player_data in data.items():
    for match in player_data["OUT"]:
        champion_won = match["champion"]
        champion_lost = match["vsChampion"]
        matchup = (champion_won, champion_lost)
        matchups[matchup] = matchups.get(matchup, 0) + 1
    for match in player_data["IN"]:
        champion_won = match["vsChampion"]
        champion_lost = match["champion"]
        matchup = (champion_won, champion_lost)
        matchups[matchup] = matchups.get(matchup, 0) + 1


top_5_matchups = sorted(matchups, key=matchups.get, reverse=True)[:5]

# Stampa le prime 5 tuple comparse più volte
print("Top 5 matchups:")
for matchup in top_5_matchups:
    print(matchup, matchups[matchup], "~", matchups.get((matchup[1], matchup[0]), 0))

# Trova il matchup meno bilanciato
most_imbalanced_matchup = max(
    matchups, key=lambda x: abs(matchups[x] - matchups.get((x[1], x[0]), 0))
)

# Calcola la percentuale di vittorie sul numero di match affrontati
vittorie = matchups[most_imbalanced_matchup]
sconfitte = matchups.get((most_imbalanced_matchup[1], most_imbalanced_matchup[0]), 0)
numero_partite = vittorie + sconfitte
percentuale_vittorie = vittorie / numero_partite * 100

# Stampa il matchup meno bilanciato e la percentuale di vittorie
print("Matchup meno bilanciato:", most_imbalanced_matchup)
print("Numero di vittorie:", vittorie)
print("Numero di sconfitte:", sconfitte)
print("Numero di partite affrontate:", numero_partite)
print("Percentuale di vittorie sul numero di partite affrontate:", percentuale_vittorie)

import matplotlib.pyplot as plt

# Campione di interesse
champion_of_interest = "Khazix"

# Trova i campioni affrontati dal campione di interesse
opponents = {
    matchup[1]: occurrences
    for matchup, occurrences in matchups.items()
    if matchup[0] == champion_of_interest
}

# Calcola il totale delle occorrenze
total_occurrences = sum(opponents.values())

# Calcola l'1% del totale
threshold = 0.01 * total_occurrences

# Raggruppa i campioni che rappresentano meno dell'1% in "others"
others_occurrences = sum(
    occurrences for occurrences in opponents.values() if occurrences < threshold
)
others_labels = [
    label for label, occurrences in opponents.items() if occurrences < threshold
]

# Rimuovi i campioni affrontati meno dell'1% dal dizionario
opponents = {
    label: occurrences
    for label, occurrences in opponents.items()
    if occurrences >= threshold
}

# Aggiungi la categoria "others" al dizionario
opponents["others"] = others_occurrences

# Crea un grafico a torta per visualizzare i campioni affrontati
labels = list(opponents.keys())
occurrences = list(opponents.values())

plt.figure(figsize=(8, 8))
plt.pie(occurrences, labels=labels, autopct="%1.1f%%")
plt.title(f"Campioni affrontati da {champion_of_interest}")
plt.show()
