import psycopg
from main import riot_name, riot_tag, player_id
def get_db_connection():
    """Establish a database connection.
    Use your preferred password and your PostgreSQL database name.
    """
    try:
        conn = psycopg.connect(
                dbname="riot_tracker", #Your database name
                user="postgres",       #Default user is "postgres".
                password="Aurora@2008" #Your PGAdmin/Postgres password
        )
        print("Connection established to the Database")
        return conn
    except psycopg.Error as e:
        print(f"Connection failed: {e}, Please check your info in the psycopg.connect section.")
        raise
def database_ini():
    """initiates the database with all the necessary tables and columns,
    further instructions at README(DB) on the GitHub repo.
    run the following "db_ini" on the console for starting the database.
    """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE player_data (
                        puuid VARCHAR(90) PRIMARY KEY,
                        username VARCHAR(16),
                        tag VARCHAR(5))
                    """)
        cur.execute("""
                    CREATE TABLE champion_data (
                        id SMALLINT PRIMARY KEY,
                        name VARCHAR(16),
                        wins INTEGER,
                        games_played INTEGER,
                        average_damage_dealt INTEGER,
                        average_damage_taken INTEGER,
                        win_rate NUMERIC(5,2),
                        pick_rate NUMERIC(5,2),
                        avg_kills SMALLINT,
                        avg_deaths SMALLINT,
                        avg_assists SMALLINT)
                    """)
        conn.commit()
def player_validation():       #Validates the player id, checking if it is already present on the database.
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT username, tag 
            FROM player_data
            WHERE username = %s AND tag = %s
            """,
            (riot_name, riot_tag)
        )
        result = cur.fetchone()
        if result is None:
                cur.execute(
                    """
                    INSERT INTO player_data(puuid, username, tag)
                    VALUES (%s, %s, %s)
                    """,
                    (riot_name, riot_tag)
                )
        conn.commit()
#def player_data_insert():     #Inserts the player data in to the database
    #conn = get_db_connection()
