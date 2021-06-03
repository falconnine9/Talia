import discord


async def send_message(msg, desc=None, channel=None, title=None, img=None, thumbnail=None, footer=None, footer_icon=None, fields=None):
    embed = discord.Embed(color=discord.Colour.purple())
    
    if desc is not None:
        embed.description = desc
    
    if title is not None:
        embed.title = title
    
    if img is not None:
        embed.set_image(url=img)
    
    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    
    if footer is not None:
        if footer_icon is None:
            embed.set_footer(text=footer)
        else:
            embed.set_footer(text=footer, icon_url=footer_icon)

    if fields is not None:
        for field in fields:
            embed.add_field(name=field[0], value=field[1])
    
    if channel is not None:
        return await channel.send(embed=embed)
    else:
        if msg is None:
            return None
        return await msg.channel.send(embed=embed)


async def send_error(msg, desc=None, channel=None, title=None):
    embed = discord.Embed(color=discord.Colour.red())
    
    if desc is not None:
        embed.description = desc
    
    if title is not None:
        embed.title = title
    
    if channel is not None:
        return await channel.send(embed=embed)
    else:
        if msg is None:
            return None
        return await msg.channel.send(embed=embed)


async def edit_message(msg, desc=None, title=None, img=None, thumbnail=None, footer=None, footer_icon=None, fields=None):
    embed = discord.Embed(color=discord.Colour.purple())
    
    if desc is not None:
        embed.description = desc
    
    if title is not None:
        embed.title = title
    
    if img is not None:
        embed.set_image(url=img)
    
    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    
    if footer is not None:
        if footer_icon is None:
            embed.set_footer(text=footer)
        else:
            embed.set_footer(text=footer, icon_url=footer_icon)

    if fields is not None:
        for field in fields:
            embed.add_field(name=field[0], value=field[1])
    
    if msg is None:
        return
    
    await msg.edit(embed=embed)


async def edit_error(msg, desc=None, title=None):
    embed = discord.Embed(color=discord.Colour.red())
    
    if desc is not None:
        embed.description = desc
    
    if title is not None:
        embed.title = title
    
    if msg is None:
        return
    
    await msg.edit(embed=embed)


async def invalid_use(msg, help_info, pre_msg):
    if len(help_info["args"]) == 0:
        await send_error(msg, f"{pre_msg}\n\n**Usage**: `{help_info['usage']}`", title="Invalid use")
    else:
        arg_list = "\n".join([f"`{arg}`: {help_info['args'][arg]}" for arg in help_info["args"]])
        await send_error(msg, f"{pre_msg}\n\n**Usage**: `{help_info['usage']}`\n\n**Arguments**\n{arg_list}", title="Invalid use")