import requests
from api import riot_api
analyzed_matches = set()
def get_matches_list(player_id, api_key): #Returns list of match ids
    match_list_api = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"
    match_request = match_list_api + player_id + '/ids?start=0&count=20&api_key=' + api_key
    tempMatches = requests.get(match_request)
    matches = tempMatches.json()
    return matches
def get_player_id(username, tag):
    acc_data = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}?api_key={riot_api}"
    response = requests.get(acc_data)
    if response.status_code == 200:
        pass
    elif response.status_code == 429:
        print("Error fetching match details: Rate limit exceeded")
    else:
        print("Error fetching match details:", response.status_code)
        return 0
    account = response.json()
    player_id = account['puuid']
    return player_id
def get_matches(matches, api_key): #Returns match data as a dictionary
    match_api = "https://americas.api.riotgames.com/lol/match/v5/matches/"
    match_request = match_api + matches + '?api_key=' + api_key
    response = requests.get(match_request)
    if response.status_code == 200:
        return response.json()  # Returns match data
    else:
        print("Error fetching match details:", response.status_code)
        return None
def player_input():
    riot_name = input("Please type your riot username: ")
    riot_tag = input("Please type your riot tag: ")
    return riot_name, riot_tag
