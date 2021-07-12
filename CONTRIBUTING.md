# Contributing
This guide provides direction on how to keep Talia's code and git repository clean and consistent.
Following this guide is important when contributing to Talia, as well as using common sense and good judgement.


## Submitting issues
[Github issues](https://guides.github.com/features/issues/) are the way that new features and bugs are reported and
tracked. They are managed by repository administrators and can be commented on or added to by anyone.

When submitting an issue, whether it be a bug report or new feature, there are a few things to keep in mind
 - **Use a simple but descriptive title**. Something like "New feature" won't work because that's all people see.
   Whereas something like "Add X feature to Y command" is a lot more eye catching and has a higher chance
   of being seen by repository administrators.
 - **Have an informative description**. Describe the bug or feature. If it was a bug, explain what you were doing when
   you found it, or where it is in the code. Or if it's a feature, explain the feature exactly. Remember that you can
   have markdown styling in the description.
 - **Don't duplicate issues or features**. Make sure that there isn't already an issue for your feature/bug. If you
   are suggesting a feature, make sure that it doesn't already exist


## Submitting code
Make sure that all the code you submit follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) styling guide. As
well as some extensions to styling that can be found below.

### Pull Requests
Code contributions can be submitted in the form of a
[pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).
All pull requests need to follow certain parameters. Pull requests that do not give enough information will be denied.
 - **Provide a descriptive title**. In a short sentence, describe what is being added in the PR.
 - **Describe the changes made in the code**. In the description, explain what you've you added, removed, or changed.
 - **Follow code styling**. Make sure all the code that you've submitted follows PEP 8 styling and any extra styling
   guides found here. You can also look in the source code to see examples.

### Commit messages
All commit messages need to have the following features
 - **A title with the proper prefix and information**. Look at the table below for what prefixes are for what situations.
   Titles should also have what has been changed
 - (Not required, but it's nice) **A short description on the changes**

| Name  | Usage                         |
|:----- |:----------------------------- |
| feat  | A new feature added           |
| fix   | A fix has been applied        |
| meta  | Should only be used by admins |
| refac | Refactoring code              |

Commit messages should have (but don't need) a scope. For example `feat(command)`. All the scopes can be found in the
table below

| Name         | Usage                            |
|:------------ |:-------------------------------- |
| command      | A new command or command changes |
| docs         | An update to the docs            |
| dependencies | Dependency changes               |
| service      | Service changes                  |

A full commit message would be: `fix(docs): Spelling errors in README.md`



## Code styling
There are a certain few styling rules (outside PEP 8) that NEED to be followed. Below is a list of situations and what
style to follow for them.

### New files
Each file should have a block comment header. An example
```python
"""
Talia Discord Bot
GNU General Public License v3.0
loop.py (Routine)
"""
```

All imports should be in alphabetical order, with local imports being at the bottoms. An example
```python
import asyncio
import discord
import os
from Utils import guild, user
from Storage import help_list
```

If you're making a new command file, it needs to include 3 global variables. All other variables should be private
(Prefixed with an underscore). These 3 global variables are shown in the example below
```python
name = "info"
dm_capable = True


async def run(bot, msg, conn):
    pass
```