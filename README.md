# Heimdall Tracker 👁️

*A League of Legends stats tracker powered by Riot Games API, PostgreSQL, and Python*

## What is Heimdall
  #### *Heimdall Tracker is a data-driven tool that fetches and analyzes player match history, champion performance, and win rates using Riot Games’ official API. Designed for players and analysts interested on having their own personal dataset, it organizes data into a PostgreSQL database and provides actionable insights through a clean CLI, I have plans for a future web application but development has not started yet due to time constraints.*

### **Key Features:**
✔ **Player Stats**: Win rates, KDA, and match history analysis.  
✔ **Champion Tier Lists**: Auto-generated from aggregated data.  
 ✔ **PostgreSQL Integration**: Efficient storage and querying of match data via the usage of the Psycopg library.  
 ✔ **Python Backend:** API calls, data processing and analysis via the utilization of the Web method.  

### **Why "Heimdall"?**
*In Norse mythology, Heimdall is the all-seeing guardian. Like its namesake, this tracker watches over your League data.*

### Prerequisites:
   *PostgreSQL (v12+)*   
   *PgAdmin4 (Recommended for DB management)*  
   *Python 3.10+*   
### Quick Start:   
 *Clone the Repository*
```diff
 git clone https://github.com/nyxm7/Heimdall-Tracker.git
 cd Heimdall-Tracker
```
### Configure Database Connection:
 *Go to the database.py file and change the following details:*
```diff
def get_db_connection():
        conn = psycopg.connect(
                dbname="riot_tracker", #Your database name
                user="postgres",       #Default user is "postgres".
                password="postgres" #Your PGAdmin/Postgres password
        )
```
### Initialize Database:
*Run the script and select "Initialize Database" from the menu:*
### All finished:
⭐*Please leave a star, it would be really appreciated*⭐
