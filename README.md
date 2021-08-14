# Talia
**Talia is currently undergoing a major redo. All contributions will be denied. It is not suggested that you use the current code**

A customizable economy discord bot

Some features of Talia include
- **Basic economy**: You can apply for customized jobs and work for coins or buy customized pickaxes and do some mining in different locations with them.
- **Gambling**: You can play games such as blackjack, roulette, flipping coins and rolling dice. Or bet against other players with pet races and pet duels.
- **Family**: Create a family tree in your server.
- **Random fun stuff**: A feature to convert images to ASCII art versions of them.
- **Highly customizable**: Almost everything in Talia can be customized on the dashboard.

By default, Talia's prefix is **t!**, but that can be changed.

Invite Talia [here](https://discord.com/api/oauth2/authorize?client_id=840430636422266910&permissions=260852673617&scope=bot)

## Running Talia
If you want to host Talia on your own, follow this guide (This is not recommended, as many Talia features depend on other not open source things). Some of these commands may need to be changed from `python3` to `python` if you're on Windows.

1. If you don't have python 3.9 already installed, you can download it [here](https://www.python.org/downloads/). Check if it's installed with `python3 --version`
2. Download the source code and create a **.env** file in the src directory (Or any directory that includes the main.py file)
3. Install all necessary dependancies with `python3 -m pip install -r requirements.txt`
4. Add the required environment variables to the .env file, see below
   ```
   TOKEN=Your bot token
   DB_HOST=Host address of the MySQL database
   DB_NAME=Database name
   DB_USER=The user you want to connect with
   DB_PASS=The user password
   ```
5. If the database is not already set up with all the tables, start Talia with `python3 main.py --tables`. But if everything is ready, start Talia with `python3 main.py`

## Made with
- [discord.py](https://github.com/Rapptz/discord.py) - Wrapper for the Discord API
- [Discord API](https://discord.com/developers/docs/intro) - API for discord bots
- [MySQL](https://www.mysql.com/) - Database service
