import random

from Utils import user, timer, message, abc, other


async def run(bot, msg, conn):
    mining_timer = timer.load_timer(f"mine.{msg.author.id}", conn)

    if mining_timer is not None:
        await message.send_error(msg, f"You need to rest for {timer.load_time(mining_timer.time)} before mining again")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if userinfo.pickaxe is None:
        await message.send_error(msg, "You need a pickaxe equipped to mine\n(You can buy one with the `pickaxe` command)")
        return

    earned_coins = round(random.randint(1, 450) * (other.load_multi(userinfo, conn) * userinfo.pickaxe.multiplier))
    earned_xp = round(random.randint(1, 20) * (other.load_multi(userinfo, conn) * userinfo.pickaxe.multiplier))
    emojis = other.load_emojis(bot)

    await message.send_message(msg, f"""You did some mining in the caves
+{earned_coins} {emojis.coin}
+{earned_xp} XP""", title="Mined")

    user.set_user_attr(msg.author.id, "coins", userinfo.coins + earned_coins, conn, False)
    user.set_user_attr(msg.author.id, "xp", userinfo.xp + earned_xp, conn)

    cooldown_time = random.randint(80, 120) * 60
    cooldown_time -= cooldown_time * ((userinfo.pickaxe.speed / 10) - 0.1)

    if cooldown_time > 0:
        new_timer = abc.Timer(f"mine.{msg.author.id}", cooldown_time, msg.author.id, None)
        timer.new_timer(new_timer, conn)