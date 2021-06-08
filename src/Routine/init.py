import json
import os
import sqlite3
import sys

from Utils import other

config_file = {
    "token": None,
    "owners": [],
    "db_path": None,
    "backups": {
        "interval": 0,
        "path": None
    },
    "links": {},
    "full_logging": False
}

tables = {
    "guilds": {
        "id": "INTEGER NOT NULL PRIMARY KEY",
        "prefix": "TEXT",
        "disabled_channels": "TEXT"
    },
    "users": {
        "id": "INTEGER NOT NULL PRIMARY KEY",
        "coins": "INTEGER",
        "xp": "INTEGER",
        "level": "INTEGER",
        "edu_level": "INTEGER",
        "job": "TEXT",
        "pickaxe": "TEXT",
        "achievements": "TEXT",
        "inventory": "TEXT",
        "fusion_level": "INTEGER",
        "multiplier": "REAL",
        "company": "TEXT",
        "showcase": "TEXT",
        "hourly": "INTEGER",
        "daily": "INTEGER",
        "partner": "INTEGER",
        "parents": "TEXT",
        "children": "TEXT"
    },
    "timers": {
        "name": "TEXT NOT NULL PRIMARY KEY",
        "time": "INTEGER",
        "user": "INTEGER",
        "meta": "TEXT"
    },
    "edu_timers": {
        "id": "INTEGER NOT NULL PRIMARY KEY",
        "time": "INTEGER",
        "edu_level": "INTEGER"
    },
    "invest_timers": {
        "id": "INTEGER NOT NULL PRIMARY KEY",
        "time": "INTEGER",
        "coins": "INTEGER",
        "multiplier": "REAL"
    },
    "companies": {
        "discrim": "TEXT NOT NULL PRIMARY KEY",
        "name": "TEXT",
        "ceo": "INTEGER",
        "members": "TEXT",
        "invites": "TEXT",
        "date_created": "TEXT",
        "multiplier": "REAL"
    },
    "log": {
        "id": "INTEGER NOT NULL PRIMARY KEY",
        "command": "TEXT",
        "user": "INTEGER",
        "guild": "INTEGER",
        "date": "TEXT"
    }
}


def config():
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


def db():
    conn = sqlite3.connect(other.load_config().db_path)
    cur = conn.cursor()

    for table in tables:
        values = ",".join([f"{value} {tables[table][value]}" for value in tables[table]])
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({values})")

    conn.commit()