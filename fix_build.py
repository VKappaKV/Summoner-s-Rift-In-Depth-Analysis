import json

# Carichiamo nuovamente il JSON
with open("jungler_network_noobs.json", "r") as f:
    data_modified = json.load(f)

# Modifichiamo la struttura del JSON
for player_data in data_modified.values():
    for match_list_key in ["OUT", "IN"]:
        if match_list_key in player_data:
            for match in player_data[match_list_key]:
                for key, opponent in list(match.items()):
                    if key.startswith("EUW1"):
                        # Separare l'ID della partita e il giocatore avversario
                        match["matchID"] = key
                        match["vs"] = opponent
                        # Rimuovere la vecchia chiave
                        del match[key]

# Salviamo il JSON modificato
modified_path = "jungler_network_noobs.json"
with open(modified_path, "w") as f:
    json.dump(data_modified, f, indent=4)

modified_path
