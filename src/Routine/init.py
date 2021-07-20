"""
Talia Discord Bot
GNU General Public License v3.0
init.py (Routine)

Initializing for the program
"""
import json
import os
import mysql.connector
import sshtunnel
import sys
from Utils import other

config_file = {
    "token": None,
    "owners": [],
    "db": {
        "host": None,
        "user": None,
        "password": None,
        "database": None,
        "ssh_username": None,
        "ssh_password": None
    },
    "backups": {
        "interval": 0,
        "database": None
    },
    "links": {},
    "full_logging": False,
    "cache_size": 1000
}

tables = {
    # Main tables
    "guilds": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "prefix": "MEDIUMTEXT",
        "disabled_channels": "MEDIUMTEXT",
        "shop": "MEDIUMTEXT",
        "CONSTRAINT guilds_pk": "PRIMARY KEY (id)"
    },
    "users": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "coins": "BIGINT UNSIGNED",
        "xp": "INTEGER",
        "level": "INTEGER",
        "edu_level": "INTEGER",
        "achievements": "MEDIUMTEXT",
        "multiplier": "REAL",
        "company": "MEDIUMTEXT",
        "hourly": "INTEGER",
        "daily": "INTEGER",
        "partner": "BIGINT UNSIGNED",
        "parents": "MEDIUMTEXT",
        "children": "MEDIUMTEXT",
        "settings": "MEDIUMTEXT",
        "color": "MEDIUMTEXT",
        "shop_info": "MEDIUMTEXT",
        "commands": "BIGINT UNSIGNED",
        "CONSTRAINT users_pk": "PRIMARY KEY (id)"
    },
    "timers": {
        "name": "VARCHAR(64) NOT NULL",
        "time": "INTEGER",
        "user": "BIGINT UNSIGNED",
        "meta": "MEDIUMTEXT",
        "CONSTRAINT timers_pk": "PRIMARY KEY (name)"
    },
    "edu_timers": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "time": "INTEGER",
        "edu_level": "INTEGER",
        "CONSTRAINT edu_timers_pk": "PRIMARY KEY (id)"
    },
    "invest_timers": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "time": "INTEGER",
        "coins": "BIGINT UNSIGNED",
        "multiplier": "REAL",
        "failed": "TINYINT",
        "loss": "REAL",
        "CONSTRAINT invest_timers_pk": "PRIMARY KEY (id)"
    },
    "companies": {
        "discrim": "VARCHAR(64) NOT NULL",
        "name": "MEDIUMTEXT",
        "ceo": "BIGINT UNSIGNED",
        "members": "MEDIUMTEXT",
        "invites": "MEDIUMTEXT",
        "date_created": "TIMESTAMP",
        "multiplier": "REAL",
        "level": "INTEGER",
        "CONSTRAINT companies_pk": "PRIMARY KEY (discrim)"
    },
    "log": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "command": "TINYTEXT",
        "user": "BIGINT UNSIGNED",
        "guild": "BIGINT UNSIGNED",
        "date": "TIMESTAMP",
        "exc_time": "INTEGER UNSIGNED",
        "CONSTRAINT log_pk": "PRIMARY KEY (id)"
    },

    # Sub tables
    "job_info": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "name": "TINYTEXT",
        "xp": "INTEGER",
        "level": "INTEGER",
        "salary": "MEDIUMTEXT",
        "cooldown": "MEDIUMTEXT",
        "CONSTRAINT job_info_pk": "PRIMARY KEY (id)"
    },
    "pickaxe_info": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "name": "TINYTEXT",
        "worth": "BIGINT UNSIGNED",
        "speed": "INTEGER",
        "multiplier": "REAL",
        "CONSTRAINT pickaxe_info_pk": "PRIMARY KEY (id)"
    },
    "pet_info": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "name": "MEDIUMTEXT",
        "worth": "BIGINT UNSIGNED",
        "type": "TINYTEXT",
        "breed": "TINYTEXT",
        "CONSTRAINT pet_info_pk": "PRIMARY KEY (id)"
    },
    "showcase_info": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "name": "MEDIUMTEXT",
        "worth": "BIGINT UNSIGNED",
        "type": "TINYTEXT",
        "stats": "MEDIUMTEXT",
        "CONSTRAINT showcase_info_pk": "PRIMARY KEY (id)"
    },
    "items": {
        "id": "BIGINT UNSIGNED NOT NULL AUTO_INCREMENT",
        "owner": "BIGINT UNSIGNED NOT NULL",
        "name": "TINYTEXT",
        "worth": "BIGINT UNSIGNED",
        "type": "TINYTEXT",
        "stats": "MEDIUMTEXT",
        "CONSTRAINT items_pk": "PRIMARY KEY (id)"
    },
    "achievements": {
        "id": "BIGINT UNSIGNED NOT NULL AUTO_INCREMENT",
        "owner": "BIGINT UNSIGNED NOT NULL",
        "name": "MEDIUMTEXT",
        "CONSTRAINT achievements_pk": "PRIMARY KEY (id)"
    }
}


def config():
    """
    Initializes the configuration file

    1. Makes sure that if no config file exists,
     then it creates one
    2. If an external config file is given, it
     checks and make sure it exists
    3. Makes sure all the required attributes
     are in the config file
    """
    if "-config" not in sys.argv:
        if not os.path.exists("config.json"):
            with open("config.json", "w") as cfg:
                json.dump(config_file, cfg, indent=4)
            other.log("Config file created")
            exit()

    try:
        configinfo = other.load_config().cvt_dict()
    except IndexError:
        other.log("No config path given after -config", "critical")
        exit()
    except FileNotFoundError:
        other.log("There is no config file in the given location", "critical")
        exit()

    for attr in config_file:
        if attr not in configinfo:
            other.log(f"Invalid configuration file (No \"{attr}\" attribute)")


def db(conn):
    """
    Initializes the database

    1. Creates a new database cursor
    2. Creates every table if it doesn't exist
    3. Sets company invites
    4. Commits
    """
    cur = conn.cursor()

    for table in tables:
        values = ",".join([f"{value} {tables[table][value]}" for value in tables[table]])
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({values})")
    conn.commit()

    cur.execute("UPDATE companies SET invites = %s", (json.dumps([]),))
    conn.commit()


def open_main_database(db_info):
    if db_info["host"] == "localhost" or db_info["host"] == "127.0.0.1":
        other.log(f"Opening connection to local database ({db_info['database']})")
        conn = mysql.connector.connect(
            user=db_info["user"], password=db_info["password"],
            host="localhost", port=3306,
            database=db_info["database"]
        )
        other.log("Complete", "success")

    else:
        other.log(f"Establishing SSH tunnel connection to {db_info['ssh_username']}@{db_info['host']}")
        with sshtunnel.SSHTunnelForwarder(
                db_info["host"], ssh_username=db_info["ssh_username"],
                ssh_password=db_info["ssh_password"], remote_bind_address=("127.0.0.1", 22)
        ) as tunnel:
            other.log("Complete", "success")
            other.log(f"Opening connection to remote database ({db_info['database']})")
            conn = mysql.connector.connect(
                user=db_info["user"], password=db_info["password"],
                host=db_info["host"], port=3306,
                database=db_info["database"]
            )
            other.log("Complete", "success")

    return conn