"""
Talia Discord Bot
GNU General Public License v3.0
init.py (Routine)

Initializing for the program
"""
import json
import os
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
        "path": None
    },
    "links": {},
    "full_logging": False
}

tables = {
    "guilds": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "prefix": "MEDIUMTEXT",
        "disabled_channels": "MEDIUMTEXT",
        "aliases": "MEDIUMTEXT",
        "shop": "MEDIUMTEXT",
        "CONSTRAINT guilds_pk": "PRIMARY KEY (id)"
    },
    "users": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "coins": "BIGINT UNSIGNED",
        "xp": "INTEGER",
        "level": "INTEGER",
        "edu_level": "INTEGER",
        "job": "MEDIUMTEXT",
        "pickaxe": "MEDIUMTEXT",
        "achievements": "MEDIUMTEXT",
        "inventory": "MEDIUMTEXT",
        "fusion_level": "INTEGER",
        "multiplier": "REAL",
        "company": "MEDIUMTEXT",
        "showcase": "MEDIUMTEXT",
        "hourly": "INTEGER",
        "daily": "INTEGER",
        "partner": "BIGINT UNSIGNED",
        "parents": "MEDIUMTEXT",
        "children": "MEDIUMTEXT",
        "settings": "MEDIUMTEXT",
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
        "coins": "INTEGER UNSIGNED",
        "multiplier": "REAL",
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
        "CONSTRAINT companies_pk": "PRIMARY KEY (discrim)"
    },
    "log": {
        "id": "BIGINT UNSIGNED NOT NULL",
        "command": "MEDIUMTEXT",
        "user": "BIGINT UNSIGNED",
        "guild": "BIGINT UNSIGNED",
        "date": "TIMESTAMP",
        "CONSTRAINT log_pk": "PRIMARY KEY (id)"
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