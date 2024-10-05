import json

def check_data_validity(data):
    for player, player_data in data.items():
        # Verifica se il giocatore contiene tutte le informazioni necessarie
        if "INFO" not in player_data or "OUT" not in player_data or "IN" not in player_data:
            print(f"Errore: Dati mancanti per il giocatore {player}")
            continue

        # Verifica se l'attributo "tier" è presente nelle informazioni del giocatore
        if "tier" not in player_data["INFO"]:
            print(f"Errore: 'tier' mancante per il giocatore {player}")

        # Verifica gli archi "games_won" per ciascun arco uscente (OUT)
        for match in player_data["OUT"]:
            if "games_won" not in match:
                print(f"Errore: Attributo 'games_won' mancante per l'arco uscente del giocatore {player}")
            elif not isinstance(match["games_won"], list):
                print(f"Errore: Attributo 'games_won' non è una lista per l'arco uscente del giocatore {player}")

        # Verifica gli archi "games_won" per ciascun arco entrante (IN)
        for match in player_data["IN"]:
            if "games_won" not in match:
                print(f"Errore: Attributo 'games_won' mancante per l'arco entrante del giocatore {player}")
            elif not isinstance(match["games_won"], list):
                print(f"Errore: Attributo 'games_won' non è una lista per l'arco entrante del giocatore {player}")

# Carica il JSON creato con il tuo codice
with open("jungler_network.json", "r") as f:
    data = json.load(f)

# Esegui il controllo sulla validità dei dati
check_data_validity(data)
