import os

import dotenv

from talia.util.console import log

_req_vars = [
    "TOKEN",
    "DB_HOST",
    "DB_NAME",
    "DB_USER",
    "DB_PASS"
]


def load_environ():
    log("Loading environment variables")
    dotenv.load_dotenv()
    for var in _req_vars:
        assert var in os.environ, f"{var} not in .env"