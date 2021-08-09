import os

import dotenv

_req_vars = [
    "TOKEN",
    "DB_HOST",
    "DB_NAME",
    "DB_USER",
    "DB_PASS"
]


def load_environ():
    dotenv.load_dotenv()
    for var in _req_vars:
        assert var in os.environ, f"{var} not in .env"