# Talia
Join the discord

[![Discord Link](https://raw.githubusercontent.com/Talia-Team/Talia/main/assets/discord%20link.png)](https://discord.gg/7FqgBCVfvY)

## Setup
1. Install all dependencies with `python3 -m pip install -r requirements.txt`
2. Run `python3 Talia.py`, this will create a file in the same directory called "config.json"
3. Fill in all the sections with their necessary requirements
4. Run Talia.py again. If everyone worked correctly, you will see "Ready"

## Configuration Attributes
- `token`: The discord bot token
- `owners`: A list of discord ID's of users with owner permissions
- `db_path`: The path to the sqlite database file
- `backups`: Information for backups
  - `interval`: The interval that backups occur (0 to disable them)
  - `path`: The path that the backups will be placed in
- `links`: A dictionary of links that will be shown in some commands