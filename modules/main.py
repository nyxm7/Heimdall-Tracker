import requests
from api import riot_api
from functions import get_matches_list, get_matches
api_key = riot_api
start_acc_data = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
on = True
while on:
    riot_name = input("Please type your riot username: ")
    riot_tag = input("Please type your riot tag(BR1, EUW1): ")
    acc_data = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_name}/{riot_tag}?api_key={api_key}"
    response = requests.get(acc_data)
    if response.status_code == 200:
        pass
    else:
        print("Error fetching match details:", response.status_code)
        continue
    account = response.json()
    player_id = account['puuid']

    matches = get_matches_list(player_id,api_key)
    wins = 0
    games_played = 0
    for counter in range(20):
        match_data = get_matches(matches, api_key, counter)
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
        print(f"\nMatch:{counter + 1}")
        print(f"Match Stats:")
        print(f"Champion: {player_stats['champion']}")
        print(f"Lane: {player_stats['lane']}")
        if player_stats['gameType'] == "CHERRY":
            print("Gamemode: Arena")
        else:
            print(f"Gamemode: {player_stats['gameType']}")
        print(f"Result: {'Victory' if player_stats['win'] else 'Defeat'}")
        if player_stats['win']:
            games_played += 1
            wins += 1
        else:
            games_played += 1
        print(f"KDA: {player_stats['kills']}/{player_stats['deaths']}/{player_stats['assists']}")
        print(f"Damage: {player_stats['damage']}")
        print(f"KDA Ratio: {player_stats['kda']:.2f}")
    print(f"Your winrate was {(wins / games_played) * 100}% over the last 20 games")
