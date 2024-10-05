import json
import timeline_player_comparison as tp

# Ricarichiamo il JSON fornito
with open("tryout_timeline.json", "r") as f:
    timeline_data = json.load(f)


def convert_positions_format(kill_positions):
    converted_positions = []

    for positions in kill_positions:
        converted_positions.append(list(positions))

    return converted_positions


def extract_kill_positions(player_id1, player_id2, data):
    early_game_positions = []
    mid_late_game_positions = []

    frames = data["info"]["frames"]
    frame_interval = data["info"]["frameInterval"] / 1000  # Convertiamo in secondi

    # Estrai le posizioni delle kill dai frames
    for i, frame in enumerate(frames):
        current_time = i * frame_interval
        for event in frame.get("events", []):
            if event.get("type") == "CHAMPION_KILL":
                killer_id = event.get("killerId")
                assisting_participants = event.get("assistingParticipantIds", [])

                # Controlla se uno dei giocatori specificati ha partecipato alla kill
                if (
                    killer_id in [player_id1, player_id2]
                    or player_id1 in assisting_participants
                    or player_id2 in assisting_participants
                ):
                    position = (event["position"]["x"], event["position"]["y"])

                    # Classifica la kill in base al minutaggio
                    if current_time < 14 * 60:  # Prima di 14 minuti
                        early_game_positions.append(position)
                    else:
                        mid_late_game_positions.append(position)

    return {
        "early": convert_positions_format(early_game_positions),
        "late": convert_positions_format(mid_late_game_positions),
    }


with open("jungler_network_pros.json", "r") as t:
    data = json.load(t)
early_kp = []
late_kp = []
for player, player_data in data.items():
    for match in player_data["OUT"]:
        response = tp.get_match_timeline(match=match["matchID"])
        result = extract_kill_positions(
            player_id1=match["index"], player_id2=match["vs_index"], data=response
        )
        for early_kills in result["early"]:
            early_kp.append(early_kills)
        for late_kills in result["late"]:
            late_kp.append(late_kills)
        print("match ", match["matchID"], "done!")
    for match in player_data["IN"]:
        response = tp.get_match_timeline(match=match["matchID"])
        result = extract_kill_positions(
            player_id1=match["index"], player_id2=match["vs_index"], data=response
        )
        for early_kills in result["early"]:
            early_kp.append(early_kills)
        for late_kills in result["late"]:
            late_kp.append(late_kills)
        print("match ", match["matchID"], "done!")

with open("visualizzazioni/kill_positions/early_kills", "w") as e:
    json.dump(early_kp, e)

with open("visualizzazioniNoobs/kill_positions/late_kills", "w") as l:
    json.dump(late_kp, l)
