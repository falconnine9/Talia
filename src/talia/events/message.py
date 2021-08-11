from main import client
from talia.obj.guild import Guild
from talia.obj.user import User
from talia.util.guild import get_guild, get_prefix, new_guild
from talia.util.user import get_user, get_user_base, get_uid, new_user


@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    if msg.guild is None:
        return

    prefix = get_prefix(msg.guild.id, conn=client.conn, confirm=True)
    if not msg.content.startswith(prefix):
        return

    msg.content = msg.content[len(prefix):].strip()
    args = msg.content.split(" ")
    args[0] = args[0].lower()

    if args[0] in client.commands.keys():
        command = client.commands[args[0]]
    else:
        if args[0] in client.aliases.keys():
            command = client.aliases[args[0]]
        else:
            return

    cur = client.conn.cursor()
    gi, gi_change = _verify_guild(msg.guild.id, cur)
    ui, ui_change = _verify_user(msg.author.id, msg.guild.id,  cur)
    mi_change = _verify_mentioned(msg, cur)

    if gi_change or ui_change or mi_change:
        client.conn.commit()

    await command.func(args, msg, gi, ui)


def _verify_guild(id_, cur):
    gi = get_guild(id_, cur)

    if gi is None:
        gi = Guild.default()
        gi.id = id_
        new_guild(gi, cur)
        return gi, True

    return gi, False


def _verify_user(id_, guild, cur):
    ui = get_user(id_, guild, cur)

    if ui is None:
        ui = User.default()
        ui.guild = guild
        ui.user = id_
        new_user(ui, cur)
        ui.id = get_uid(id_, guild, cur)
        return ui, True

    return ui, False


def _verify_mentioned(msg, cur):
    changed = False

    for mention in msg.mentions:
        ui = get_user_base(mention.id, msg.guild.id, cur)
        if ui is None:
            ui = User.default()
            ui.guild = msg.guild.id
            ui.user = mention.id
            new_user(ui, cur)
            changed = True

    return changed