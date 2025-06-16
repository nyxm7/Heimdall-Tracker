import psycopg
import time

from functions import get_player_id, get_matches_list
from functions import get_matches
from api import riot_api
def get_db_connection():
    """Establish a database connection.
    Use your preferred password and your PostgreSQL database name.
    """
    try:
        conn = psycopg.connect(
                dbname="riot_tracker", #Your database name
                user="postgres",       #Default user is "postgres".
                password="postgres" #Your PGAdmin/Postgres password
        )
        return conn
    except psycopg.Error as e:
        print(f"Connection failed: {e}, Please check your info in the psycopg.connect section.")
        raise

def player_validation(riot_name, riot_tag):
    """
    Validates the player id, checking if it is already present on the database
    If it isn't, it is then added to it.
    """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM player_data
            WHERE username = %s AND tag = %s
            """,
            (riot_name, riot_tag)
        )
        player = cur.fetchone()
        if player is None: # Inserts player data to the database
            puuid = get_player_id(riot_name, riot_tag)
            cur.execute(
                """
                INSERT INTO player_data(puuid, username, tag)
                VALUES (%s, %s, %s)
                """,
                (puuid, riot_name, riot_tag)
            )
            conn.commit()
            return puuid
        elif player is not None:
                cur.execute("""
                    SELECT puuid FROM player_data
                    WHERE username = %s AND tag = %s
                    """,
                    (riot_name, riot_tag)
                )
                puuid = cur.fetchone()
                return puuid[0]

def match_data_validation(match_data):
    """
    Verifies if the match data is in the database.
    If not, inserts match data for all participants.
    """
    conn = get_db_connection()
    match_id = match_data['metadata']['matchId']
    player_ids = match_data['metadata']['participants']

    with conn.cursor() as cur:
        # Check if match exists
        cur.execute(
            "SELECT * FROM match_data WHERE match_data_id = %s",
            (match_id,)
        )
        response = cur.fetchone()

        if response is None:
            # Insert data for each participant
            for participant in match_data['info']['participants']:
                if participant['win'] is True:
                    win = 1
                else:
                    win = 0
                cur.execute(
                    """
                    INSERT INTO match_data (
                        match_data_id, champion, username, tag, puuid, lane, 
                        win, gameType, damage, kills, deaths, assists
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        match_id,
                        participant['championName'],
                        participant.get('riotIdGameName'),
                        participant.get('riotIdTagline'),
                        participant['puuid'],
                        participant['teamPosition'],
                        participant['win'],
                        match_data['info']['gameMode'],
                        participant['totalDamageDealtToChampions'],
                        participant['kills'],
                        participant['deaths'],
                        participant['assists'],
                    )
                )
                cur.execute(
                    """
                    INSERT INTO champion_data (id, wins, games_played, kills, deaths, assists, damage_dealt)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        wins = champion_data.wins + EXCLUDED.wins,
                        games_played = champion_data.games_played + EXCLUDED.games_played,
                        kills = champion_data.kills + EXCLUDED.kills,
                        deaths = champion_data.deaths + EXCLUDED.deaths,
                        assists = champion_data.assists + EXCLUDED.assists,
                        damage_dealt = champion_data.damage_dealt + EXCLUDED.damage_dealt
                    """,
                    (participant['championId'], win, 1, participant['kills'], participant['deaths'],
                     participant['assists'], participant['totalDamageDealtToChampions'])
                )
            conn.commit()
    conn.close()
    return player_ids
def web_method():
    puuid_queue = []
    processed_puuid = set()
    conn = get_db_connection()
    counter = 1
    cosmetic = 1
    with conn.cursor() as cur:
        cur.execute(
            "SELECT puuid FROM match_data ORDER BY random() LIMIT 1"
        )
        response = cur.fetchone()
        if response:
            puuid_queue.append(response)
        while puuid_queue:
            current_puuid = puuid_queue.pop()
            if current_puuid in processed_puuid:
                continue
            processed_puuid.add(current_puuid)
            match_list = get_matches_list(str(current_puuid), riot_api)
            for match in match_list:
                cur.execute(
                    """SELECT puuid FROM match_data 
                    WHERE match_data_id = %s LIMIT 1
                    """,
                    (match,)
                )
                answer = cur.fetchone()
                if answer is not None:
                    puuid_queue.append(answer)
                    continue
                else:
                    match_data = get_matches(match, riot_api)
                    puuids = match_data_validation(match_data)
                    print(cosmetic)
                    if counter >= 80:
                        print("Entering sleep, PLEASEEEEEEEE Riot, give me permanent API key, so that i don't have to do this everytime.")
                        time.sleep(120)
                        counter = 1
                    counter += 1
                    cosmetic += 1
                    for e in range(len(puuids)):
                        puuid_queue.append(puuids[e])
                    for i in puuids:
                        cur.execute(
                            """SELECT puuid FROM player_data 
                            WHERE puuid = %s
                            """,
                            (i,)
                        )
                        resp = cur.fetchone()
                        if resp is None:
                            part_index = match_data['metadata']['participants'].index(i)
                            cur.execute(
                                """
                                INSERT INTO player_data(puuid, username, tag)
                                VALUES (%s, %s, %s)
                                """,
                                (i, match_data['info']['participants'][part_index]['riotIdGameName'],
                                 match_data['info']['participants'][part_index]['riotIdTagline'])
                            )
                        conn.commit()
