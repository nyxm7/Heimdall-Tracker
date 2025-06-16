from api import riot_api
from functions import get_matches_list, get_matches, player_input
from database import player_validation, match_data_validation, web_method, get_db_connection
from database_ini import database_ini


class Menu:
    def __init__(self):
        self.running = True
        self.menu_options = {
            "1": {"text": "Checking Champion Stats ", "action": self.display_champion},
            "2": {"text": "Get match history", "action": self.match_history},
            "3": {"text": "Check Tier List", "action": self.tier_list},
            "4": {"text": "Initialize database", "action": self.db_ini},
            "5": {"text": "Utilize Web method (Read repo for info)", "action": self.web},
            "6": {"text": "Exit", "action": self.exit_menu}
        }

    def display_menu(self):
        print("\n--- Menu ---")
        for key, option in self.menu_options.items():
            print(f"{key}. {option['text']}")

    def display_champion(self):
        conn = get_db_connection()
        choice = input("Which champion: ")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT wins, games_played, kills, deaths, damage_dealt, assists FROM champion_data
                WHERE name = %s
                """,
                (choice,)
            )
            response = cur.fetchall()
            if not response:
                print(f"No data found for champion '{choice}', Check capitalization Ex: Rakan")
                return
            for champion in response:
                wins, games_played, kills, deaths, damage_dealt, assists = champion
                win_rate = (wins / games_played) * 100 if games_played > 0 else 0
                kda = ((kills + assists) / deaths) if deaths > 0 else (kills + assists)
                avg_damage = damage_dealt / games_played if games_played > 0 else 0
                print(f"\n--- {choice} ---")
                print(f"Win Rate: {win_rate:.2f}%")
                print(f"Games Played: {games_played}")
                print(f"Average Kills: {kills / games_played:.1f}" if games_played > 0 else "Average Kills: 0")
                print(f"Average Deaths: {deaths / games_played:.1f}" if games_played > 0 else "Average Deaths: 0")
                print(f"Average Assits: {assists / games_played:.1f}" if games_played > 0 else "Average Assists: 0")
                print(f"KDA Ratio: {kda:.2f}")
                print(f"Average Damage: {avg_damage:,.0f}")
    def match_history(self):
        name, tag = player_input()
        player_id = player_validation(name, tag)
        matches = get_matches_list(player_id, riot_api)
        wins = 0
        games_played = 0
        for idx, i in enumerate(matches):
            match_data = get_matches(matches[idx], riot_api)
            match_data_validation(match_data)
            part_index = match_data['metadata']['participants'].index(player_id)
            player_stats = {
                'champion': match_data['info']['participants'][part_index]['championName'],
                'username': match_data['info']['participants'][part_index]['riotIdGameName'],
                'tag': match_data['info']['participants'][part_index]['riotIdTagline'],
                'puuid': match_data['info']['participants'][part_index]['puuid'],
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
            print(f"\nMatch:{idx + 1}")
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
        try:
            print(f"Your winrate was {(wins / games_played) * 100}% over the last 20 games")
        except ZeroDivisionError:
            pass

    def tier_list(self):
        conn = get_db_connection()
        tier_map = {}
        s_list = []
        a_list = []
        b_list = []
        c_list = []

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT name, wins, games_played FROM champion_data
                WHERE games_played > 0
                """
            )
            data = cur.fetchall()

            for champion in data:
                name, wins, games_played = champion
                win_rate = wins / games_played
                tier_map[name] = win_rate

                # Categorize champions by win rate
                if win_rate >= 0.52:
                    s_list.append(name)
                elif win_rate >= 0.50:
                    a_list.append(name)
                elif win_rate >= 0.48:
                    b_list.append(name)
                else:
                    c_list.append(name)

        conn.close()
        print(f"S-tier: {', '.join(s_list)}")
        print(f"A-tier: {', '.join(a_list)}")
        print(f"B-tier: {', '.join(b_list)}")
        print(f"C-tier: {', '.join(c_list)}")

    def db_ini(self):
        print("Be sure to have all your details on get_db_connection (Located on database.py) correct.")
        print("initializing database....")
        database_ini()
        print("Check your PgAdmin")

    def web(self):
        print("Please check the GitHub repo for FAQ")
        web_method()

    def exit_menu(self):
        print("Exiting...")
        self.running = False

    def run(self):
        while self.running:
            self.display_menu()
            choice = input("Enter your choice: ")

            selected_option = self.menu_options.get(choice)
            if selected_option:
                selected_option["action"]()
            else:
                print("Invalid choice. Please try again.")
