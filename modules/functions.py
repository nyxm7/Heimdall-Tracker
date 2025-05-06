import requests

def get_matches_list(player_id, api_key): #Returns list of match ids
    match_List_api = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"
    match_request = match_List_api + player_id + '/ids?start=0&count=20&api_key=' + api_key
    tempMatches = requests.get(match_request)
    matches = tempMatches.json()
    return matches

def get_matches(matches, api_key, counter): #Returns match data as a dictionary
    match_api = "https://americas.api.riotgames.com/lol/match/v5/matches/"
    match_request = match_api + matches[counter] + '?api_key=' + api_key
    response = requests.get(match_request)
    if response.status_code == 200:
        return response.json()  # Returns match data
    else:
        print("Error fetching match details:", response.status_code)
        return None