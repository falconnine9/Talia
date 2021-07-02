# Contributing
All contributions should take place on the [GitHub repository](https://github.com/Talia-Team/Talia).
This guide ensures that all of Talia's code follows the same pattern.
Below, you will find sections for each piece of code and what pattern to follow

As well as the guides below, all code styling should follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)

If you don't find something here for formatting, looking for examples in the source files can help

## Making a new file
Add the start of each file, there should be a doc string with file information in it.
Below is an example
```python
"""
Talia Discord Bot
GNU General Public License v3.0
handle.py (Routine)

Handles events (Such as commands sent)
"""
```
Switch out "handle.py" for what the file name is and "(Routine)" with what folder it's in.
Also add a short description of the file's purpose

## Imports
Imports should be under the doc string at the start of the file with no whitespace in between

Imports should be sorted in alphabetical order

External imports should be on top, and Talia imports should be below (`from Storage` should always be **after** `from Utils`)

Module imports should have their own import statement on each line, and "from" imports should have each thing it's importing split with commas.
An example is below
```python
import asyncio
import discord
import random
from Utils import user, message, other
from Storage import help_list
```

Imports from Utils should be in the following order:
- **guild**
- **user**
- **company**
- **timer**
- **message**
- **abc**
- **other**

## Strings
Very short strings should use newline characters (`\n`) to add line breaks

Long strings should use doc strings to add newline characters

If a string includes variables in the string, the string should be an f-string using f-string components. 
If the string has no variables, it should use a regular string. Multiple examples are below
```python
# Short string with no variables
"Lorem ipsum\ndolor sit amet"

# Long string with no variables
"""Lorem ipsum dolor sit amet, 
consectetur adipiscing elit. 
Mauris eget pharetra nibh. Fusce congue placerat augue ac fermentum. 
Phasellus vel sem quis lacus malesuada condimentum."""

# Short string with variables
f"Lorem ipsum dolor {variable1} sit amet"

# Long string with variables
"""Lorem ipsum dolor sit amet, 
consectetur adipiscing elit. {variable1}
Mauris eget pharetra nibh. Fusce congue placerat augue ac fermentum. 
Phasellus vel sem {variable2} quis lacus malesuada condimentum."""
```

## Creating a command
Each command must include the following
- A file in the correct category with the command name (ex. info.py)
- Command information in the file
- A run method that takes 3 parameters: **bot**, **msg**, **conn**
- A spot in the \_\_init\_\_.py file within that command category
- A variable with the command name in the help list
- A spot in the command list

### Command File
As said [above](#making-a-new-file), the start of the file must include a doc string with the correct information

The file must also include command information which is surrounded by a comment.
An example is below
```python
#   Command Information   #
name = "command"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #
```
The name should be the name of the command, and dm_capable will decide if it can be run in DMs or not

Any variables for the command should be 1 line away from the bottom comment.
An example is below
```python
#   Command Information   #
name = "command"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #

variable1 = ""

variable2 = [
    "stuff",
    "other stuff",
    "more stuff"
]
```

The file must also include a run method (It won't work if it doesn't have this).
The command needs to take 3 parameters: **bot**, **msg**, **conn**.
An example is below
```python
async def run(bot, msg, conn):
```
- The bot parameter is the discord client object (discord.Client)
- The msg parameter is the message that the user sent (discord.Message)
- The conn parameter is a connection to the MySQL database (mysql.connector.MySQLConnection)


## Certain variable names
There are a few variable names which should always be used

- **person**: The return value from `bot.get_user` or `bot.fetch_user`
- **userinfo**: When you load a user with `user.load_user` (From msg.author.id)
- **personinfo**: When you load a user with `user.load_user` (From person.id)
- **guildinfo**: When you load a user with `guild.load_guild`
- **companyinfo**: When you load a company with `company.load_company`
- **split_data**: When you make the message content into arguments with `msg.content.split`