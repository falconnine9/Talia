# Talia
**TALIA IS CURRENTLY UNDERGOING MAJOR REDOING, NO SOURCE CODE WILL BE AVAILABLE FOR A WHILE**

Join the discord!

[![Discord Link](https://raw.githubusercontent.com/Talia-Team/Talia-Assets/main/icons/discord%20link.png)](https://discord.gg/7FqgBCVfvY)

## Setup
(Note that all calls to `python3` may need to be changed to `python` if you're on Windows.)

1. Ensure that Python is installed with `python3 --version`. (If it's not, you can download it [here](https://www.python.org/downloads/))
2. Install dependencies with `python3 -m pip install -r requirements.txt`.
3. Setup a MySQL database (If you need to download it, you can find it [here](https://www.mysql.com/downloads/)).
4. Run `Talia.py` (In `src/`) with `python3 Talia.py`. This will create a configuration (`config.json`) file in the same directory.
5. Fill in all the sections. (A guide on that can be found [here](#config)).
6. Run `python3 Talia.py` again to start the bot, and if everything worked correctly you will see "Ready".

## Config
A description for each section of the configuration file.  
- **token**: Discord client token.
- **owners**: A list of discord ID's with complete owner access.
- **db**
  - **host**: IP to the server where it's located. (Can be "localhost" for a local database.)
  - **user**: The MySQL user you want to use for access.
  - **password**: The password of the MySQL user.
  - **database**: Which database to use.
  - **ssh_username**: The username to use for access to a remote database through SSH. (Only needed if accessing a remote database.)
  - **ssh_password**: The password to use for access to a remote database through SSH. (Only needed if accessing a remote database.)
- **backups**
  - **interval**: The interval (in seconds) to make a backup of the database.
  - **database**: The database to make a backup in.
- **links**: A dictionary of links to show.
- **full_logging**: Log **EVERYTHING**.

## Using
Things Talia uses:
- [Python](https://www.python.org/) - High level programming language.
- [MySQL](https://www.mysql.com/) - Database system.

## Dependencies
Python packages that Talia uses:
- [discord.py](https://pypi.org/project/discord.py/)/[discord-components](https://pypi.org/project/discord-components/) - API wrapper for Discord.
- [colorama](https://pypi.org/project/colorama/) - For colored text in the terminal.
- [psutil](https://pypi.org/project/psutil/) - Getting system information.
- [mysql](https://pypi.org/project/mysql/)/[mysql-connector-python](https://pypi.org/project/mysql-connector-python/) - For connecting Python to MySQL.
- [sshtunnel](https://pypi.org/project/sshtunnel/) - Package for opening SSH connections.
