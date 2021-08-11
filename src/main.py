import os
import sys

from bot import client
from talia.init import database, env


if __name__ == "__main__":
    from talia.commands import get_all
    from talia.events import get_all
    from talia.service import get_all

    with open("header.txt") as hf:
        print(hf.read())

    env.load_environ()
    client.conn = database.get_connection()

    if "--tables" in sys.argv:
        database.create_tables(client.conn)

    client.run_wrapper(os.environ["TOKEN"])