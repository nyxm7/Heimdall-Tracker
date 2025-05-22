from api import riot_api
from functions import get_matches_list, get_matches, get_player_id
#from database import database_ini
on = True
while on:
    riot_name = input("Please type your riot username: ")
    riot_tag = input("Please type your riot tag: ")
    player_id = get_player_id(riot_name,riot_tag)
    matches = get_matches_list(player_id,riot_api)
    wins = 0
    games_played = 0
    for counter in range(20):
        match_data = get_matches(matches, riot_api, counter)
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
        if player_stats['lane'] == '':
            pass
        else:
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
