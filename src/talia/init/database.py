import os

import mysql.connector

from talia.util.console import log


def get_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"], database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"], password=os.environ["DB_PASS"]
    )


def create_tables(conn):
    log("Creating tables")
    cur = conn.cursor()
    with open("talia/init/tables.sql") as sql_f:
        sql_data = sql_f.read()
    for query in sql_data.split(";"):
        cur.execute(query.strip())
    conn.commit()