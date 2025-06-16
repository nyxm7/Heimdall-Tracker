from database import get_db_connection

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
        tag VARCHAR(5),
        id SERIAl,
        """)
        cur.execute("""
        CREATE TABLE champion_data (
        id SMALLINT PRIMARY KEY,
        name VARCHAR(16),
        wins INTEGER,
        games_played INTEGER,
        damage_dealt INTEGER,
        kills INTEGER,
        deaths INTEGER,
        assists INTEGER)
        """)
        cur.execute("""
        CREATE TABLE match_data (
        match_data_id TEXT,
        username VARCHAR(20),
        tag VARCHAR(7),
        puuid TEXT,
        champion VARCHAR(16),
        lane VARCHAR(10),
        win BOOLEAN,
        gameType VARCHAR(20),
        damage INTEGER,
        kills SMALLINT,
        deaths SMALLINT,
        assists SMALLINT)
        """)
        conn.commit()
    conn.close()
