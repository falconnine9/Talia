"""
Talia Discord Bot
GNU General Public License v3.0
mine.py (Commands/Earning)

mine command
"""
import random
from Utils import user, timer, subtable, message, abc, other

name = "mine"
dm_capable = True

_artifacts = [
    {
        "name": "Copper Artifact",
        "worth": [100, 200],
        "chance": 0.4
    },
    {
        "name": "Iron Artifact",
        "worth": [150, 300],
        "chance": 0.3
    },
    {
        "name": "Gold Artifact",
        "worth": [500, 1000],
        "chance": 0.1
    },
    {
        "name": "Diamond Artifact",
        "worth": [2000, 5000],
        "chance": 0.05
    },
    {
        "name": "Mithril Artifact",
        "worth": [7000, 10000],
        "chance": 0.03
    },
    {
        "name": "Glowing Artifact",
        "worth": [8000, 10000],
        "chance": 0.03
    },
    {
        "name": "Silicon Artifact",
        "worth": [9000, 11000],
        "chance": 0.02
    },
    {
        "name": "Uranium Artifact",
        "worth": [10000, 13000],
        "chance": 0.02
    },
    {
        "name": "Sodium Artifact",
        "worth": [10000, 14000],
        "chance": 0.02
    },
    {
        "name": "Neon Artifact",
        "worth": [10000, 15000],
        "chance": 0.02
    },
    {
        "name": "Magnesium Artifact",
        "worth": [14000, 18000],
        "chance": 0.01
    }
]


async def run(args, bot, msg, conn, guildinfo, userinfo):
    mining_timer = timer.load_timer(f"mine.{msg.author.id}", conn)

    if mining_timer is not None:
        await message.send_error(msg, f"You need to rest for {timer.load_time(mining_timer.time)} before mining again")
        return

    if userinfo.pickaxe is None:
        await message.send_error(msg,
            "You need a pickaxe equipped to mine\n(You can buy one with the `pickaxe` command)"
        )
        return

    artifact_chance = random.randint(1, 3)

    earned_coins = round(random.randint(1, 450) * (other.load_multi(userinfo, conn) * userinfo.pickaxe.multiplier))
    earned_xp = round(random.randint(1, 20) * (other.load_multi(userinfo, conn) * userinfo.pickaxe.multiplier))

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + earned_coins, conn, False)
    user.set_user_attr(msg.author.id, "xp", userinfo.xp + earned_xp, conn, False)

    cooldown_time = random.randint(80, 120) * 60
    cooldown_time -= cooldown_time * ((userinfo.pickaxe.speed / 10) - 0.1)

    if cooldown_time > 0:
        new_timer = abc.Timer(f"mine.{msg.author.id}", cooldown_time, msg.author.id, None)
        timer.new_timer(new_timer, conn, False)

    emojis = other.load_emojis(bot)
    await message.send_message(msg, f"You did some mining in the caves\n+{earned_coins:,} {emojis.coin}\n+{earned_xp:,} XP",
        title="Mined"
    )

    if len(userinfo.inventory) < 40 and artifact_chance == 1:
        chance = random.random()
        total_chance = 0.0

        for artifact in _artifacts:
            total_chance += artifact["chance"]
            if chance < total_chance:
                item = abc.Item(
                    artifact["name"],
                    random.randint(artifact["worth"][0], artifact["worth"][1]),
                    "artifact", {}, None
                )
                subtable.new_item(msg.author.id, item, conn, False)
                await message.send_message(msg, f"You found a {artifact['name']}!")
                break

    conn.commit()