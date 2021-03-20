import base64
import json
import random
import discord, datetime, time
from discord.ext import commands
from discord.ext.commands import bot
import requests
import os

CHANNEL_ID = '822799450195361802'

bot = commands.Bot(command_prefix='c!',
                   description="This is TDA BOT V2, better than the V1. This is so special because I coded it all myself!")

STARTUP_MESSAGE = 'Ready'

start_time = time.time()


@bot.event
async def on_ready():
    print(STARTUP_MESSAGE)
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name=" TDA game idk forgot the name "))


def timedelta_str(dt):
    """time uptime"""
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days, hours, minutes, sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days, hours, minutes, sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days, hours, minutes, sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days, hours, minutes, sec)


@bot.command()
async def uptime(ctx):
    """Displays bot uptime."""
    global start_time
    await ctx.send(timedelta_str(datetime.datetime.now() - start_time))


@bot.command(description='Add a suggestion.')
async def suggest(ctx, *, suggestion):
    """"Suggestion command. Sends an suggestion to an channel that might be added soon"""
    await ctx.channel.purge(limit=1)
    channel = discord.utils.get(ctx.guild.text_channels, name='tda-bot-suggestions')
    suggestEmbed = discord.Embed(colour=0xFF0000)
    suggestEmbed.set_author(name=f'Suggested by {ctx.message.author}', icon_url=f'{ctx.author.avatar_url}')
    suggestEmbed.add_field(name='New suggestion!', value=f'{suggestion}')
    await channel.send(embed=suggestEmbed)


@bot.command(helpinfo='Mad? throw a table against people.')
async def throw(ctx):
    '''
    Mad? throw a table against people.
    '''
    await ctx.send("```(╯°□°)╯︵ ┻━┻```")


@bot.command(helpinfo='Shows member count.')
async def members(ctx):
    '''
    Shows member count.
    '''
    await ctx.send(f"{ctx.guild.member_count}")


@bot.command(helpinfo='Be an assassin')
async def kill(ctx, *, user='You'):
    '''
    Kills the player, minecraft style
    '''
    await ctx.send((user) + ' fell out of the world')


@bot.command(helpinfo='Picks randomly between multiple choices')
async def choose(ctx, *choices: str):
    '''
    Picks randomly from all choices provided.
    '''
    await ctx.send((random.choice(choices)) + ', I choose you!')


@bot.command(helpinfo='Shows MC account info, skin and username history', aliases=['skin', 'mc'])
async def minecraft(ctx, username='Shrek'):
    '''
    Shows MC account info, skin and username history
    '''
    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'
                        .format(username)).json()['id']

    url = json.loads(base64.b64decode(requests.get(
        'https://sessionserver.mojang.com/session/minecraft/profile/{}'
            .format(uuid)).json()['properties'][0]['value'])
                     .decode('utf-8'))['textures']['SKIN']['url']

    names = requests.get('https://api.mojang.com/user/profiles/{}/names'
                         .format(uuid)).json()
    history = "**Name History:**\n"
    for name in reversed(names):
        history += name['name'] + "\n"

    await ctx.send('**Username: `{}`**\n**Skin: {}**\n**UUID: {}**'.format(username, url, uuid))
    await ctx.send(history)


@bot.command(helpinfo='shows info about the user you pinged or yourself.')
async def userinfo(ctx, *, user: discord.Member = None):
    '''
    shows info about the user you pinged or yourself.
    '''
    if user is None:
        user = ctx.author
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)


@bot.command(helpinfo='shows bots ping')
async def ping(ctx):
    '''
    Shows bots ping
    '''
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')


@bot.command(helpinfo='calculates for you')
async def sum(ctx, numOne: int, numTwo: int):
    '''
    If you're too lazy to do math then here you go
    '''
    await ctx.send(numOne + numTwo)


@bot.command()
async def roles(context):
    """Lists the current roles on the server."""

    roles = context.message.guild.roles
    result = "The roles on this server are: "
    for role in roles:
        result += role.name + ", "
    await context.send(result)


@bot.command(helpinfo='Sends the groups link')
async def group(ctx):
    '''
    Sends the group's link
    '''
    await ctx.send('https://www.roblox.com/groups/6268298/The-Drones-Army#!/about')


@bot.command(pass_context=True, helpinfo='Shows all banned people')
async def gbans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await bot.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title="List of The Banned Idiots", description=x, color=0xFFFFF)
    return await bot.say(embed=embed)


@bot.command(helpinfo='Shows info about the server.')
async def info(ctx):
    '''
    Shows info about the server.
    '''
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Shows info about the server",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    await ctx.send(embed=embed)


bot.run(os.environ('ODIyNTY4NTQxMjgyNjMxNzgw.YFUKpg.ZXheKQ4l9vunQOYfvrrq_VlYLG4'))
