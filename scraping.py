from riotwatcher import LolWatcher, ApiError
import time
import json

Out = "OUT"
In = "IN"
Info = "INFO"
lol_watcher = LolWatcher("RGAPI-3e23770e-241b-4ac3-a74a-8450f9041736")


def get_account(username):
    try:
        return lol_watcher.summoner.by_name("euw1", username)
    except ApiError as err:
        if err.response.status_code == 429:
            print("We should retry in {} seconds.".format(err.headers["Retry-After"]))
            return get_account(username)
        else:
            return None


def get_puuid(account_info):
    if "puuid" in account_info:
        return account_info["puuid"]
    else:
        print("No puuid found in account info")
        return None


def get_account_info(summonerID):
    try:
        return lol_watcher.league.by_summoner("euw1", encrypted_summoner_id=summonerID)
    except ApiError as err:
        if err.response.status_code == 429:
            print("We should retry in {} seconds.".format(err.headers["Retry-After"]))
            return get_account_info(summonerID)
        else:
            return None


def get_matchlist(puuid, start_at):
    try:
        return lol_watcher.match.matchlist_by_puuid(
            "EUROPE",
            puuid,
            queue=420,
            type="ranked",
            start_time=1690101004,
            end_time=1690446600,
            start=start_at,  # dalle 8:30 del 26/07 al 27/07
        )
    except ApiError as err:
        if err.response.status_code == 429:
            print("We should retry in {} seconds.".format(err.headers["Retry-After"]))
            return get_matchlist(puuid)
        else:
            print("errore a questo punto")
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


def is_match_won(match, index):
    return match["info"]["participants"][index]["win"]


def get_winning_team(match_response):
    winners = []
    for summoner in match_response["info"]["participants"]:
        if summoner["win"]:
            winners.append(summoner["summonerName"])
    return winners


def get_general_info(jsonResponse):
    return {
        "gameDuration": jsonResponse["info"]["gameDuration"],
        "gameStartTimestamp": jsonResponse["info"]["gameStartTimestamp"],
    }


def get_losing_team(match_response):
    losers = []
    for summoner in match_response["info"]["participants"]:
        if not summoner["win"]:
            losers.append(summoner["summonerName"])
    return losers


def get_opponent_in_role(match, posix):
    role = match["info"]["participants"][posix]["teamPosition"]
    for index, summoner in enumerate(match["info"]["participants"]):
        if summoner["teamPosition"] == role and posix != index:
            return summoner["summonerName"], index
    return None


def get_team_bans(match, index):
    team = match["info"]["participants"][index]["teamId"]
    for teamPick in match["info"]["teams"]:
        if teamPick["teamId"] == team:
            return [ban["championId"] for ban in teamPick["bans"]]


def get_champion(match, index):
    return match["info"]["participants"][index]["championName"]


def get_summonerId(match, index):
    return match["info"]["participants"][index]["summonerId"]


def get_rankedQ_stats(data):
    for item in data:
        if item["queueType"] == "RANKED_SOLO_5x5":
            return {
                "tier": item["tier"],
                "rank": item["rank"],
                "LP": item["leaguePoints"],
                "wins": item["wins"],
                "losses": item["losses"],
            }

def get_player_key_performance(match, index):
    timestamp = timestamp_to_min(match["info"]["gameDuration"])
    return {
        "kda" : match["info"]["participants"][index]["challenges"]["kda"],
        "gpm" : match["info"]["participants"][index]["challenges"]["goldPerMinute"],
        "cs" :  match["info"]["participants"][index]["totalMinionsKilled"],
        "CSpm" : match["info"]["participants"][index]["totalMinionsKilled"]/timestamp,
        "vs" : match["info"]["participants"][index]["visionScore"],
        "VSpm" : match["info"]["participants"][index]["challenges"]["visionScorePerMinute"],
    }

def timestamp_to_min(timestamp_in_secondi):
    minuti = timestamp_in_secondi // 60
    secondi = timestamp_in_secondi % 60
    formato_mm_ss = "{:02d}:{:02d}".format(int(minuti), int(secondi))
    return minuti

checked_players = {}
starting_players = []
list_checked_players = []
# 1st iteration handpicked: jankos
#starting_players = ["LuvFlakkedCheeks"]

# 2nd iteration starting from checkpoint file
with open('search_list.json','r') as k:
    starting_players = json.load(k)
with open('jungler_network.json','r') as t:
    checked_players = json.load(t)
    list_checked_players = checked_players.keys()
account_search_set = set()
account_search_set.update(starting_players["Current"] + starting_players["Next"])
#account_search_set.update(starting_players)
player_node = checked_players
#player_node = {}
searched_players = set(list_checked_players)
#searched_players = set()
progress_checkpoint = {"Current": [], "Next": []}
checked_matches = []
while len(account_search_set) > 0:
    print("\n nuova iterazione \n ")
    search_list = list(account_search_set)
    new_players = set()
    for search_account in search_list:
        searched_players.add(search_account)
        # inizializzo il dict e la lista
        player_node[search_account] = {Info: {}, Out: [], In: []}
        # ho lo username, estraggo i dati per ottenere il puuid
        account = get_account(search_account)
        if account is None:
            account_search_set.discard(search_account)
            continue
        puuid = get_puuid(account)
        if puuid is None:
            account_search_set.discard(search_account)
            continue
        encryptedID = account["id"]
        account_queue_stats = get_rankedQ_stats(get_account_info(encryptedID))
        player_node[search_account][Info] = account_queue_stats 
        print("cerco i match di: ", search_account, " puuid: ", puuid)
        # ho il puuid estraggo i match giocati
        matches = get_matchlist(puuid=puuid, start_at=0)
        if matches is None:
            account_search_set.discard(search_account)
            continue
        print("matches : \n ", len(matches))
        if len(matches) == 20:
            matches.extend(get_matchlist(puuid=puuid, start_at=20))
        for match in matches:
            # per ogni match estraggo le informazioni per capire se il match è stato vinto
            if match in checked_matches:
                continue
            match_info = get_matchinfo(match)
            if match_info is None:
                account_search_set.discard(search_account)
                continue
            # dalle informazioni estraggo anche i dati fondamentali
            index = match_info["metadata"]["participants"].index(puuid)
            if match_info["info"]["participants"][index]["teamPosition"] != "JUNGLE":
                continue
            match_result = True if is_match_won(match_info, index) else False
            result_is = "WIN" if match_result else "LOSS"
            print("MATCH: ", match, " : ", result_is)
            result = get_opponent_in_role(match_info, index)
            if result is None:
                continue 
            playerToExtract, vs_index = result 
            champion = get_champion(match_info, index)
            general_info = get_general_info(match_info)
            vs_champion = get_champion(match_info, vs_index)
            bans = get_team_bans(match_info, index)
            vs_bans = get_team_bans(match_info, vs_index)
            vs_queue_stats = get_rankedQ_stats(get_account_info(get_summonerId(match_info,vs_index)))
            key_stats = get_player_key_performance(match_info, index)
            vs_key_stats = get_player_key_performance(match_info, vs_index)
            print("preso le key stats, aggiungo il dict del match: ", match)
            match_dict = {
                match: playerToExtract,
                "vs_queue_stats": vs_queue_stats,
                "champion": champion,
                "info": general_info,
                "vsChampion": vs_champion,
                "index": index,
                "vs_index": vs_index,
                "vs_id": get_summonerId(match_info, vs_index),
                "bans": bans,
                "vs_bans": vs_bans,
                "performance" : key_stats,
                "vs_performance" : vs_key_stats
            }

            print("Player to add: ", playerToExtract)
            new_players.add(playerToExtract)
            # Aggiorno il nodo
            if match_result:
                player_node[search_account][Out].append(match_dict)
            else:
                player_node[search_account][In].append(match_dict)
            time.sleep(0.1)
            progress_checkpoint["Current"] = list(account_search_set)
            #progress_checkpoint["Next"] = list(new_players)
            with open("jungler_network_2.json", "w") as f:
                json.dump(player_node, f, indent=4)

            with open("search_list.json", "w") as t:
                json.dump(progress_checkpoint, t, indent=4)
            checked_matches.append(match)
        account_search_set.discard(search_account)
    new_players.difference_update(
        searched_players
    )  # Rimuovi i giocatori già ricercati da new_players
    account_search_set.update(
        new_players
    )  # Aggiorna account_search_set con i nuovi giocatori
