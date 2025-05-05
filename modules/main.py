import requests
from api import riot_api
start_acc_data = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
on = True
while on:
    riot_name = input("Please type your riot username: ")
    riot_tag = input("Please type your riot tag(BR1, EUW1): ")
    acc_data = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_name}/{riot_tag}?api_key={riot_api}"
    api_url = acc_data
    response = requests.get(acc_data)
    account = response.json()
    player_id = account['puuid']

    def get_matches_list():
        match_List_api = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"
        match_request = match_List_api + player_id + '/ids?start=0&count=20&api_key=' + riot_api
        tempMatches = requests.get(match_request)
        matches = tempMatches.json()
        return matches

    matches = get_matches_list()
    choice = True
    while choice:
        game_choice = int(input("What game would you want to check ? (0 to 20, 0 newest, 20 oldest): "))
        if 0 <= game_choice <= 20:
            print("Ok!")
            choice = False
        else:
            print("invalid choice, try again!")
    def get_matches(matches):
        match_api = "https://americas.api.riotgames.com/lol/match/v5/matches/"
        match_request = match_api + matches[game_choice] + '?api_key=' + riot_api
        response = requests.get(match_request)
        if response.status_code == 200:
            return response.json()  # Returns match data
        else:
            print("Error fetching match details:", response.status_code)
            return None

    match_data = get_matches(matches)
    part_index = match_data['metadata']['participants'].index(player_id)
    player_stats = {
        'champion': match_data['info']['participants'][part_index]['championName'],
        'lane': match_data['info']['participants'][part_index]['teamPosition'],
        'win': match_data['info']['participants'][part_index]['win'],
        'gameType': match_data['info']['gameMode'],
        'damage': match_data['info']['participants'][part_index]['totalDamageDealtToChampions'],
        'kills': match_data['info']['participants'][part_index]['kills'],
        'deaths': match_data['info']['participants'][part_index]['deaths'],
        'assists': match_data['info']['participants'][part_index]['assists'],
        'kda': (match_data['info']['participants'][part_index]['kills'] +
               match_data['info']['participants'][part_index]['assists']) /
               max(1, match_data['info']['participants'][part_index]['deaths'])
    }
    print(f"\nMatch Stats:")
    print(f"Champion: {player_stats['champion']}")
    print(f"Lane: {player_stats['lane']}")
    print(f"Gamemode:{player_stats['gameType']}")
    print(f"Result: {'Victory' if player_stats['win'] else 'Defeat'}")
    print(f"KDA: {player_stats['kills']}/{player_stats['deaths']}/{player_stats['assists']}")
    print(f"Damage: {player_stats['damage']}")
    print(f"KDA Ratio: {player_stats['kda']:.2f}")

    keep_going = input("Do you wish to look at any other matches ? Type 'y' or 'n'")
    if keep_going == "y":
        pass
    if keep_going == "n":
        on = False

