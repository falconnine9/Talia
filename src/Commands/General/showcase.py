from Utils import user, message, abc
from Storage import help_list


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.showcase, "No item given")
        return

    if split_data[1].lower() == "remove":
        userinfo = user.load_user(msg.author.id, conn)

        if userinfo.showcase is None:
            await message.send_error(msg, "You don't have an item in your showcase")
            return

        userinfo.inventory.append(userinfo.showcase)
        user.set_user_attr(msg.author.id, "inventory", userinfo.inventory, conn, False)
        user.set_user_attr(msg.author.id, "showcase", abc.Item(
            None, 0, "box_item", {}
        ).cvt_dict(), conn)

        await message.send_message(msg, "You removed the item from your showcase", title="Removed")

    try:
        item = int(split_data[1]) - 1
    except ValueError:
        await message.send_error(msg, "Invalid item ID")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if item < 0 or item > len(userinfo.inventory) - 1:
        await message.send_error(msg, "There's no item in your inventory with that ID")
        return

    if userinfo.showcase is not None:
        userinfo.inventory.append(userinfo.showcase)

    await message.send_message(msg, f"You put a {userinfo.inventory[item].name} in your showcase", title="Added")

    user.set_user_attr(msg.author.id, "showcase", userinfo.inventory[item].cvt_dict(), conn, False)
    userinfo.inventory.pop(item)
    user.set_user_attr(msg.author.id, "inventory", userinfo.inventory, conn)