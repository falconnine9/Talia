"""
Talia Discord Bot
GNU General Public License v3.0
showcase.py (Commands/General)

showcase command
"""
from Utils import user, subtable, message, abc
from Storage import help_list

name = "showcase"
dm_capable = True


async def run(args, bot, msg, conn):
    if len(args) < 2:
        await message.invalid_use(msg, help_list.showcase, "No item given")
        return

    if args[1].lower() == "remove":
        userinfo = user.load_user(msg.author.id, conn)

        if userinfo.showcase is None:
            await message.send_error(msg, "You don't have an item in your showcase")
            return

        subtable.remove_showcase(msg.author.id, conn, False)
        subtable.new_item(msg.author.id, userinfo.showcase, conn)

        await message.send_message(msg, "You removed the item from your showcase", title="Removed")
        return

    try:
        item = int(args[1]) - 1
    except ValueError:
        await message.send_error(msg, "Invalid item ID")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if item < 0 or item > len(userinfo.inventory) - 1:
        await message.send_error(msg, "There's no item in your inventory with that ID")
        return

    if userinfo.showcase is not None:
        subtable.new_item(msg.author.id, userinfo.showcase, conn, False)

    subtable.new_showcase(msg.author.id, userinfo.inventory[item], conn, False)
    subtable.remove_item(userinfo.inventory[item].id, conn)

    await message.send_message(msg, f"You put a {userinfo.inventory[item].name} in your showcase", title="Added")