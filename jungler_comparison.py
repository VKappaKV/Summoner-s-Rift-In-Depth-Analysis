import json
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import time

lol_watcher = LolWatcher("RGAPI-dbb5ef2c-fa98-4516-b501-0a29de5a4f41")  # dev key here


def get_match_timeline(match):
    try:
        return lol_watcher.match.timeline_by_match("euw1", match)
    except ApiError as err:
        if err.response.status_code == 429:
            print("We should retry in {} seconds.".format(err.headers["Retry-After"]))
            return get_match_timeline(match)
        else:
            return None


def get_matchinfo(match_id):
    try:
        return lol_watcher.match.by_id("EUROPE", match_id)
    except ApiError as err:
        if err.response.status_code == 429:
            print("We should retry in {} seconds.".format(err.headers["Retry-After"]))
            return get_matchinfo(match_id)
        else:
            return None


def get_player_index(match, player):
    # print(match["info"]["participants"])
    for summoner in match["info"]["participants"]:
        if summoner["summonerName"] == player:
            return summoner["participantId"]


def extract_team_details(team_id, data):
    tower_kills = 0
    tower_plates = 0
    dragon_kills = 0
    herald_captures = 0

    for frame in data["info"]["frames"][:15]:  # Looping directly up to 15 frames
        for event in frame["events"]:
            if event["type"] == "TURRET_PLATE_DESTROYED" and event["teamId"] == team_id:
                tower_plates += 1
            elif (
                event["type"] == "BUILDING_KILL"
                and event["buildingType"] == "TOWER"
                and event["teamId"] == team_id
            ):
                tower_kills += 1
            elif (
                event["type"] == "ELITE_MONSTER_KILL"
                and event.get("killerTeamId") == team_id
            ):
                if event["monsterType"] == "DRAGON":
                    dragon_kills += 1
                elif event["monsterType"] == "RIFTHERALD":
                    herald_captures += 1

    return {
        "tower_kills": tower_kills,
        "tower plates": tower_plates,
        "dragon_kills": dragon_kills,
        "herald_captures": herald_captures,
    }


def extract_player_details(index, data, frame_15):
    participant = frame_15["participantFrames"][str(index)]
    champion_kills = 0
    for frame in data["info"]["frames"][:15]:
        for event in frame["events"]:
            if "killerId" in event and "assistingParticipantIds" in event:
                if (
                    event["type"] == "CHAMPION_KILL"
                    and event["killerId"] == index
                    or event["type"] == "CHAMPION_KILL"
                    and index in event["assistingParticipantIds"]
                ):
                    champion_kills += 1
    return {
        "totalGold": participant["totalGold"],
        "kills": champion_kills,
        "minionsKilled": participant["minionsKilled"],
        "jungleMinionsKilled": participant["jungleMinionsKilled"],
        "level": participant["level"],
        "xp": participant["xp"],
        "teamId": 100 if index <= 5 else 200,
    }


def extract_game_details_at_15min(data, player_idx1, player_idx2):
    # Extract the frame at 15 minutes
    frame_15 = data["info"]["frames"][15] if len(data["info"]["frames"]) >= 15 else None
    if frame_15 is None or player_idx1 is None or player_idx2 is None:
        return None

    player1_details = extract_player_details(player_idx1, data, frame_15)
    player2_details = extract_player_details(player_idx2, data, frame_15)

    player1_team_details = extract_team_details(player1_details["teamId"], data)
    player2_team_details = extract_team_details(player2_details["teamId"], data)

    player1_combined = {**player1_details, **player1_team_details}
    player2_combined = {**player2_details, **player2_team_details}

    return player1_combined, player2_combined


def extract_game_details_to_excel(id, data, player_idx1, player_idx2, win):
    result = extract_game_details_at_15min(data, player_idx1, player_idx2)
    if result is None:
        return None

    player1_data, player2_data = result

    player1_data = {f"p1_{k}": v for k, v in player1_data.items()}
    player2_data = {f"p2_{k}": v for k, v in player2_data.items()}
    win_value = 1
    if not win:
        win_value = 0
    combined_data = {
        "id": id,
        **player1_data,
        **player2_data,
        "p1_wins": win_value,
    }

    # df = pd.concat([df, pd.DataFrame([combined_data])], ignore_index=True)
    return combined_data


def is_checked(match_id, data):
    for m in data:
        if m["id"] == match_id:
            return True
    return False


df = pd.read_excel("game_details.xlsx")
matches_w = []
matches_l = []
requests = 0
with open("table_data_extraction_losers3.json", "r") as l:
    matches_l = json.load(l)
with open("table_data_extraction_winners3.json", "r") as w:
    matches_w = json.load(w)
with open("jungler_network_pros.json", "r") as r:
    scraped_data = json.load(r)
    for player, player_data in scraped_data.items():
        for match in player_data["OUT"]:
            if is_checked(match["matchID"], matches_w):
                continue
            if requests % 100 == 0 and requests != 0:
                print("sleeping 2 minutes zzzz")
                time.sleep(120)
            elif requests % 20 == 0:
                print("quick nap")
                time.sleep(1)
            crawl_match = get_matchinfo(match["matchID"])
            requests += 1
            if crawl_match is None:
                continue
            index = get_player_index(crawl_match, player)
            vs_index = get_player_index(crawl_match, match["vs"])
            match_data = get_match_timeline(match["matchID"])
            requests += 1
            print("extracting OUT: ", match["matchID"], " of ", player)
            extracted_data = extract_game_details_to_excel(
                id=match["matchID"],
                data=match_data,
                player_idx1=index,
                player_idx2=vs_index,
                win=True,
            )
            if extracted_data is None:
                continue
            matches_w.append(extracted_data)
        with open("table_data_extraction_winners4.json", "w") as t:
            json.dump(matches_w, t, indent=4)
        for match in player_data["IN"]:
            if is_checked(match["matchID"], matches_l):
                continue

            if requests % 100 == 0 and requests != 0:
                print("sleeping 2 minutes zzzz")
                time.sleep(120)
            elif requests % 20 == 0:
                print("quick nap")
                time.sleep(1)

            crawl_match = get_matchinfo(match["matchID"])
            requests += 1
            if crawl_match is None:
                continue
            index = get_player_index(crawl_match, player)
            vs_index = get_player_index(crawl_match, match["vs"])
            match_data = get_match_timeline(match["matchID"])
            requests += 1
            print("extracting IN: ", match["matchID"], " of ", player)
            extracted_data = extract_game_details_to_excel(
                id=match["matchID"],
                data=match_data,
                player_idx1=index,
                player_idx2=vs_index,
                win=False,
            )
            if extracted_data is None:
                continue
            matches_l.append(extracted_data)
        with open("table_data_extraction_losers4.json", "w") as p:
            json.dump(matches_l, p, indent=4)
