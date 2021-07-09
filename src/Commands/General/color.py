"""
Talia Discord Bot
GNU General Public License v3.0
color.py (Commands/General)

color command
"""
from Utils import user, message
from Storage import help_list

name = "color"
dm_capable = True


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg, help_list.color, "No red value given")
        return

    if len(split_data) < 3:
        await message.invalid_use(msg, help_list.color, "No green value given")
        return

    if len(split_data) < 4:
        await message.invalid_use(msg, help_list.color, "No blue value given")
        return

    try:
        r = int(split_data[1])
        g = int(split_data[2])
        b = int(split_data[3])
    except ValueError:
        await message.send_error(msg, "Each color value must be a number between 0-255")
        return

    if (r < 0 or r > 255) or (g < 0 or g > 255) or (b < 0 or b > 255):
        await message.send_error(msg, "Each color value must be a number between 0-255")
        return

    user.set_user_attr(msg.author.id, "color", [r, g, b], conn)
    await message.send_message(msg, f"""Your profile color has been changed
R: {r}
G: {g}
B: {b}""", title="Color changed")