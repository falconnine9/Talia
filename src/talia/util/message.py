import discord


async def send_embed(msg, channel=None, **kw):
    if "colour" not in kw:
        kw["colour"] = (155, 89, 182)
    embed = create_embed(**kw)

    if channel is None:
        if msg is not None:
            await msg.channel.send(embed=embed)
    else:
        await channel.send(embed=embed)


async def send_embed_err(msg, channel=None, **kw):
    if "colour" not in kw:
        kw["colour"] = (231, 76, 60)
    embed = create_embed(**kw)

    if channel is None:
        if msg is not None:
            await msg.channel.send(embed=embed)
    else:
        await channel.send(embed=embed)


def create_embed(**kw):
    embed = discord.Embed()

    for param in kw:
        if param == "desc":
            embed.description = kw[param]
        elif param == "title":
            embed.title = kw[param]
        elif param == "footer":
            embed.set_footer(text=kw[param])
        elif param == "image":
            embed.set_image(url=kw[param])
        elif param == "thumbnail":
            embed.set_thumbnail(url=kw[param])
        elif param == "fields":
            for field in kw["params"]:
                embed.add_field(
                    name=field.name,
                    value=field.value,
                    inline=field.inline
                )
        elif param == "colour":
            embed.colour = discord.Colour.from_rgb(
                kw[param][0],
                kw[param][1],
                kw[param][2]
            )

    return embed