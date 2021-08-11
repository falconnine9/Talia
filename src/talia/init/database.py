import os

import mysql.connector

from talia.util.console import log


def get_connection():
    confirm = input(("Are you sure you want to connect to "
           f"{os.environ['DB_USER']}@{os.environ['DB_HOST']} "
           f"on database {os.environ['DB_NAME']} [y/n]"))
    if confirm.lower() != "y":
        raise RuntimeError("Database connection cancelled")

    log(f"Establishing connection to database {os.environ['DB_NAME']}")
    return mysql.connector.connect(
        host=os.environ["DB_HOST"], database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"], password=os.environ["DB_PASS"]
    )


def create_tables(conn):
    confirm = input(("Are you sure you want to create tables in the database "
                     "(Nothing will be overwritten) [y/n]"))
    if confirm.lower() != "y":
        return

    log("Creating tables")
    cur = conn.cursor()
    with open("talia/init/tables.sql") as sql_f:
        sql_data = sql_f.read()
    for query in sql_data.split(";"):
        cur.execute(query.strip())
    conn.commit()