from Utils import message, other
from Storage import meta, help_list

help_info = {
    "general": {
        "help": help_list.help_,
        "ping": help_list.ping,
        "info": help_list.info,
        "stats": help_list.stats,
        "inventory": help_list.inventory,
        "fuse": help_list.fuse,
        "school": help_list.school,
        "box": help_list.box,
        "leaderboard": help_list.leaderboard,
        "company": help_list.company,
        "showcase": help_list.showcase
    },
    "earning": {
        "job": help_list.job,
        "work": help_list.work,
        "heist": help_list.heist,
        "invest": help_list.invest,
        "pickaxe": help_list.pickaxe,
        "mine": help_list.mine,
        "sidejob": help_list.sidejob,
        "hourly": help_list.hourly,
        "daily": help_list.daily
    },
    "gambling": {
        "coinflip": help_list.coinflip,
        "dice": help_list.dice,
        "blackjack": help_list.blackjack
    },
    "settings": {
        "prefix": help_list.prefix,
        "channels": help_list.channels
    }
}


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await _category_list(bot, msg)

    else:
        choice = " ".join(split_data[1:]).lower()

        if choice in help_info.keys():
            await _command_list(bot, msg, choice)
            return

        for category in help_info.keys():
            if choice in help_info[category]:
                await _command_details(bot, msg, category, choice)
                return

        await message.send_error(msg, "No category/command found")


async def _category_list(bot, msg):
    cat_list = "\n".join([f"**{category[0].upper()}{category[1:]}**" for category in help_info.keys()])
    links = other.load_config().links

    if len(links) == 0:
        await message.send_message(msg,
            f"You can use `help <category>` for all commands in that category\n\n{cat_list}",
            title="Help", footer=f"Talia version {meta.version}", footer_icon=bot.user.avatar_url
        )

    else:
        str_links = " | ".join([f"[{link[0].upper()}{link[1:]}]({links[link]})" for link in links])
        await message.send_message(msg,
            f"You can use ``help <category>`` for all commands in that category\n\n{cat_list}\n\n{str_links}",
            title="Help", footer=f"Talia version {meta.version}", footer_icon=bot.user.avatar_url
        )


async def _command_list(bot, msg, choice):
    comm_list = ", ".join([f"`{command}`" for command in help_info[choice].keys()])
    await message.send_message(msg,
        f"You can use `help <command>` for details of that command\n\n{comm_list}",
        title=f"{choice[0].upper()}{choice[1:]}", footer=f"Talia version {meta.version}",
        footer_icon=bot.user.avatar_url
    )


async def _command_details(bot, msg, category, choice):
    command_info = help_info[category][choice]

    if len(command_info["args"]) == 0:
        await message.send_message(msg,
            f"**Description**: {command_info['desc']}\n**Usage**: {command_info['usage']}",
            title=choice, footer=f"Talia version {meta.version}", footer_icon=bot.user.avatar_url
        )

    else:
        arg_list = "\n".join([f"`{arg}`: {command_info['args'][arg]}" for arg in command_info["args"].keys()])
        await message.send_message(msg,
            f"**Description**: {command_info['desc']}\n**Usage**: {command_info['usage']}\n\n**Arguments**\n{arg_list}",
            title=choice, footer=f"Talia version {meta.version}", footer_icon=bot.user.avatar_url
        )