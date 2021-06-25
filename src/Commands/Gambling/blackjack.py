"""
Talia Discord Bot
GNU General Public License v3.0
blackjack.py (Commands/Gambling)
blackjack command
"""
import asyncio
import discord
import discord_components
import random
from Utils import user, message, abc, other
from Storage import help_list

#   Command Information   #
name = "blackjack"
dm_capable = True
# ~~~~~~~~~~~~~~~~~~~~~~~ #

suits = ["\u2660", "\u2663", "\u2665", "\u2666"]
values = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}


async def run(bot, msg, conn):
    split_data = msg.content.split(" ")

    if len(split_data) < 2:
        await message.invalid_use(msg,
            help_list.blackjack,
            "No bet given")
        return

    try:
        bet = int(split_data[1])
    except ValueError:
        await message.send_error(msg,
            "Invalid bet")
        return

    emojis = other.load_emojis(bot)

    if bet < 1:
        await message.send_error(msg,
            f"You need to bet at least 1 {emojis.coin}")
        return

    userinfo = user.load_user(msg.author.id, conn)

    if bet > userinfo.coins:
        await message.send_error(msg,
            f"You don't have enough coins to bet {bet} {emojis.coin}")
        return

    userinfo.coins -= bet
    user.set_user_attr(msg.author.id, "coins", userinfo.coins, conn)

    deck = []
    for suit in suits:
        for value in values:
            deck.append(abc.BJCard(value, suit, values[value]))

    dealer_cards = []
    user_cards = []

    for i in range(2):
        random_card = random.choice(deck)
        dealer_cards.append(random_card)
        deck.remove(random_card)

        random_card2 = random.choice(deck)
        user_cards.append(random_card2)
        deck.remove(random_card2)

    if _card_amount(dealer_cards) < 16:
        random_card = random.choice(deck)
        dealer_cards.append(random_card)
        deck.remove(random_card)

        if _card_amount(dealer_cards) > 21:
            await message.send_message(msg,
                f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({_card_amount(dealer_cards)})
You: {_show_all_cards(user_cards)} ({_card_amount(user_cards)})

**Dealer busted, you win!** +{round(bet * 2)} {emojis.coin}""",
                title="You win")
            user.set_user_attr(msg.author.id, "coins", userinfo.coins + round(bet * 2), conn)
            return

    if _card_amount(user_cards) == 21:
        if _card_amount(user_cards) == _card_amount(dealer_cards):
            await message.send_message(msg,
                f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({_card_amount(dealer_cards)})
You: {_show_all_cards(user_cards)} ({_card_amount(user_cards)})

**Tie** +{bet} {emojis.coin}""",
                title="Tie")
            user.set_user_attr(msg.author.id, "coins", userinfo.coins + bet, conn)
        else:
            await message.send_message(msg,
                f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({_card_amount(dealer_cards)})
You: {_show_all_cards(user_cards)} ({_card_amount(user_cards)})

**Blackjack, you win!** +{round(bet * 2 + (bet * 0.5))} {emojis.coin}""",
                title="You win")
            user.set_user_attr(msg.author.id, "coins", userinfo.coins + round(bet * 2 + (bet * 0.5)), conn)
        return

    sent_msg = await message.send_message(msg,
        f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_hidden_cards(dealer_cards)}
You: {_show_all_cards(user_cards)} ({_card_amount(user_cards)})""",
        title="Blackjack",
        components=[[
            discord_components.Button(label="Hit", style=discord_components.ButtonStyle.blue),
            discord_components.Button(label="Stand")
        ]])

    def button_check(interaction):
        if interaction.author != msg.author:
            return False

        if interaction.message != sent_msg:
            return False

        return True

    while True:
        try:
            interaction = await bot.wait_for("button_click", timeout=120, check=button_check)
        except asyncio.TimeoutError:
            await message.timeout_response(sent_msg)
            return

        userinfo = user.load_user(msg.author.id, conn)

        if interaction.component.label == "Hit":
            random_card = random.choice(deck)
            user_cards.append(random_card)
            deck.remove(random_card)
            card_amount = _card_amount(user_cards)

            if card_amount > 21:
                await message.response_edit(sent_msg, interaction, f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({_card_amount(dealer_cards)})
You: {_show_all_cards(user_cards)} ({card_amount})

**Busted, you lose**""", title="You lose")
                return

            elif card_amount == 21:
                if _card_amount(dealer_cards) == 21:
                    await message.response_edit(sent_msg, interaction, f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({_card_amount(dealer_cards)})
You: {_show_all_cards(user_cards)} ({card_amount})

**Tie** +{bet} {emojis.coin}""", title="Tie")
                    user.set_user_attr(msg.author.id, "coins", userinfo.coins + bet, conn)
                else:
                    await message.response_edit(sent_msg, interaction, f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({_card_amount(dealer_cards)})
You: {_show_all_cards(user_cards)} ({card_amount})

**Blackjack, you win!** +{bet * 2} {emojis.coin}""", title="You win")
                user.set_user_attr(msg.author.id, "coins", userinfo.coins + (bet * 2), conn)
                return

            else:
                embed = discord.Embed(description=f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_hidden_cards(dealer_cards)}
You: {_show_all_cards(user_cards)} ({card_amount})""", color=discord.Colour.purple(), title="Blackjack")
                await interaction.respond(type=7, embed=embed, components=[[
                        discord_components.Button(label="Hit", style=discord_components.ButtonStyle.blue),
                        discord_components.Button(label="Stand")
                    ]])

        elif interaction.component.label == "Stand":
            dealer_card_amount = _card_amount(dealer_cards)
            user_card_amount = _card_amount(user_cards)

            if dealer_card_amount > user_card_amount:
                await message.response_edit(sent_msg, interaction, f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({dealer_card_amount})
You: {_show_all_cards(user_cards)} ({user_card_amount})

**You lose**""", title="You lose")

            elif dealer_card_amount < user_card_amount:
                await message.response_edit(sent_msg, interaction, f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({dealer_card_amount})
You: {_show_all_cards(user_cards)} ({user_card_amount})

**You win!** +{bet * 2} {emojis.coin}""", title="You win")
                user.set_user_attr(msg.author.id, "coins", userinfo.coins + (bet * 2), conn)

            else:
                await message.response_edit(sent_msg, interaction, f"""Blackjack cost: -{bet} {emojis.coin}

Dealer: {_show_all_cards(dealer_cards)} ({dealer_card_amount})
You: {_show_all_cards(user_cards)} ({user_card_amount})

**Tie** +{bet} {emojis.coin}""", title="Tie")
                user.set_user_attr(msg.author.id, "coins", userinfo.coins + bet, conn)
            return


def _card_amount(cards):
    total = 0
    for card in cards:
        total += card.real_value
    if total > 21:
        for card in cards:
            if card.value == "A":
                total -= 10
                break
    return total


def _show_all_cards(cards):
    return " ".join([f"[{card.value}{card.suit}]" for card in cards])


def _show_hidden_cards(cards):
    card_list = []
    for i, card in enumerate(cards):
        if i >= 1:
            card_list.append(f"[#{card.suit}]")
            break
        else:
            card_list.append(f"[{card.value}{card.suit}]")
    return " ".join(card_list)